#!./env/bin/python
# Model
# Creates a schema through the sqlachemy orm. Only supports postgresql.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import ARRAY, BIGINT, TEXT, TIMESTAMP
from secret_keys import db_credentials as db
from sqlalchemy.orm import sessionmaker

connect_string = 'postgresql+psycopg2://{user}:{password}@/{dbname}'.format(
    user=db['usename'], password=db['password'], dbname=db['dbname'])
engine = create_engine(connect_string)
Base = declarative_base()


class Summoner(Base):
    __tablename__ = 'summoner'
    __table_args__ = (
        PrimaryKeyConstraint('region', 'summoner_id', name='summoner_pk'),
    )
    region = Column(TEXT, nullable=False)
    summoner_id = Column(Integer, nullable=False)
    summoner_name = Column(TEXT)
    revision_date = Column(TIMESTAMP)


class ChampionTag(Base):
    __tablename__ = 'champion_tag'
    champion_tag_id = Column(Integer, primary_key=True)
    tag = Column(TEXT)


class Champion(Base):
    __tablename__ = 'champion'
    champion_id = Column(Integer, primary_key=True)
    champion_name = Column(TEXT)
    champion_tag_ids = Column(ARRAY(Integer))


class ChampionMastery(Base):
    __tablename__ = 'champion_mastery'
    __table_args__ = (
        PrimaryKeyConstraint('summoner_region', 'summoner_id', 'champion_id',
                             name='champion_mastery_pk'),
        ForeignKeyConstraint(['summoner_region', 'summoner_id'],
                             ['summoner.region', 'summoner.summoner_id']),
    )
    summoner_region = Column(TEXT, nullable=False)
    summoner_id = Column(Integer, nullable=False)
    champion_id = Column(Integer, ForeignKey('champion.champion_id'),
                         nullable=False)

    champion_points = Column(Integer, nullable=False)
    highest_grade = Column(TEXT, nullable=False)
    last_play_time = Column(TIMESTAMP, nullable=False)


Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
