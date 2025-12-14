from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

engine = create_engine("sqlite:///data/traffic.db", echo=False)
Base = declarative_base()


class Traffic(Base):
    """Stores individual packet/traffic records"""
    __tablename__ = "traffic"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    src_ip = Column(String(45), index=True)  # IPv6 max length
    dst_ip = Column(String(45))
    src_port = Column(Integer)
    dst_port = Column(Integer)
    protocol = Column(String(20), index=True)
    packet_size = Column(Integer)
    packet_count = Column(Integer, default=1)
    avg_size = Column(Float)
    
    __table_args__ = (
        Index('idx_traffic_src_dst', 'src_ip', 'dst_ip'),
    )


class Alert(Base):
    """Stores security alerts and anomalies detected"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    alert_type = Column(String(50), index=True)  # ML_ANOMALY, RATE_LIMIT, PORT_SCAN, etc.
    severity = Column(String(20), default="medium")  # low, medium, high, critical
    src_ip = Column(String(45), index=True)
    dst_ip = Column(String(45))
    protocol = Column(String(20))
    description = Column(Text)
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime)
    
    __table_args__ = (
        Index('idx_alerts_unresolved', 'is_resolved', 'timestamp'),
    )


class SystemStats(Base):
    """Stores periodic system statistics snapshots"""
    __tablename__ = "system_stats"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    total_packets = Column(Integer, default=0)
    packets_per_second = Column(Float, default=0.0)
    anomaly_count = Column(Integer, default=0)
    protocol_breakdown = Column(Text)  # JSON string of protocol counts


class BlockedIP(Base):
    """Stores IPs that have been blocked due to suspicious activity"""
    __tablename__ = "blocked_ips"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip_address = Column(String(45), unique=True, index=True)
    blocked_at = Column(DateTime, default=datetime.utcnow)
    reason = Column(Text)
    alert_count = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime)  # Optional auto-unblock time


# Create all tables
Base.metadata.create_all(engine)

# Session factory
Session = sessionmaker(bind=engine)


# Helper functions for database operations
def get_session():
    """Get a new database session"""
    return Session()


def save_traffic(session, packet_data):
    """Save a traffic record to the database"""
    traffic = Traffic(
        src_ip=packet_data.get("src_ip"),
        dst_ip=packet_data.get("dst_ip"),
        src_port=packet_data.get("src_port"),
        dst_port=packet_data.get("dst_port"),
        protocol=packet_data.get("protocol"),
        packet_size=packet_data.get("size", 0)
    )
    session.add(traffic)
    return traffic


def save_alert(session, alert_data):
    """Save an alert to the database"""
    alert = Alert(
        alert_type=alert_data.get("type"),
        severity=alert_data.get("severity", "medium"),
        src_ip=alert_data.get("src_ip"),
        dst_ip=alert_data.get("dst_ip"),
        protocol=alert_data.get("protocol"),
        description=alert_data.get("description", "")
    )
    session.add(alert)
    return alert


def get_recent_alerts(session, limit=50):
    """Get recent unresolved alerts"""
    return session.query(Alert).filter(
        Alert.is_resolved == False
    ).order_by(Alert.timestamp.desc()).limit(limit).all()


def get_blocked_ips(session):
    """Get currently blocked IPs"""
    return session.query(BlockedIP).filter(
        BlockedIP.is_active == True
    ).all()


def block_ip(session, ip_address, reason):
    """Block an IP address"""
    existing = session.query(BlockedIP).filter(
        BlockedIP.ip_address == ip_address
    ).first()
    
    if existing:
        existing.alert_count += 1
        existing.is_active = True
        return existing
    
    blocked = BlockedIP(ip_address=ip_address, reason=reason)
    session.add(blocked)
    return blocked
