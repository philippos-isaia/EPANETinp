#!/usr/bin/python
import psycopg2
from config import config


def create_tables(tables):
    """ create tables in the PostgreSQL database"""
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()
        for value in tables:
            cur.execute(value)

        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    tables=['CREATE TABLE IF NOT EXISTS JUNCTIONS (ID VARCHAR, Elev FLOAT, Demand FLOAT, Pattern VARCHAR);',
        'CREATE TABLE IF NOT EXISTS RESERVOIRS (ID VARCHAR, Head FLOAT, Pattern VARCHAR);',
        'CREATE TABLE IF NOT EXISTS TANKS (ID VARCHAR, Elevation FLOAT, InitLevel FLOAT, MinLevel FLOAT, MaxLevel FLOAT, Diameter FLOAT, MinVol FLOAT, VolCurve VARCHAR);',
        'CREATE TABLE IF NOT EXISTS PIPES (ID VARCHAR, Node1 VARCHAR, Node2 VARCHAR, Length FLOAT, Diameter FLOAT, Roughness FLOAT, MinorLoss FLOAT, Status VARCHAR);',
        'CREATE TABLE IF NOT EXISTS PUMPS (ID VARCHAR, Node1 VARCHAR, Node2 VARCHAR, Parameters VARCHAR);',
        'CREATE TABLE IF NOT EXISTS VALVES (ID VARCHAR, Node1 VARCHAR, Node2 VARCHAR, Diameter FLOAT, Type VARCHAR, Setting FLOAT, MinorLoss FLOAT);',
        'CREATE TABLE IF NOT EXISTS DEMANDS (Junction VARCHAR, Demand FLOAT, Pattern VARCHAR, Category VARCHAR);',
        'CREATE TABLE IF NOT EXISTS STATUS (ID VARCHAR, StatusSetting VARCHAR);',
        'CREATE TABLE IF NOT EXISTS PATTERNS (ID VARCHAR, Multipliers VARCHAR);',
        'CREATE TABLE IF NOT EXISTS CURVES (ID VARCHAR, XValue FLOAT, YValue FLOAT);',
        'CREATE TABLE IF NOT EXISTS ENERGY (value VARCHAR);',
        'CREATE TABLE IF NOT EXISTS EMITTERS (Junction VARCHAR, Coefficient FLOAT);',
        'CREATE TABLE IF NOT EXISTS QUALITY (Node VARCHAR, InitQual FLOAT);',
        'CREATE TABLE IF NOT EXISTS SOURCES (Node VARCHAR, Type VARCHAR, Quality FLOAT, Pattern VARCHAR);',
        'CREATE TABLE IF NOT EXISTS REACTIONS (Type VARCHAR, Coefficient FLOAT);',
        'CREATE TABLE IF NOT EXISTS MIXING (Tank VARCHAR, Model VARCHAR, Volume FLOAT);',
        'CREATE TABLE IF NOT EXISTS COORDINATES (Node VARCHAR, XCoord FLOAT, YCoord FLOAT);',
        'CREATE TABLE IF NOT EXISTS VERTICES (Link VARCHAR, XCoord FLOAT, YCoord FLOAT);',
        'CREATE TABLE IF NOT EXISTS LABELS (XCoord FLOAT, YCoord FLOAT, Label VARCHAR, Anchor VARCHAR);']
    create_tables(tables)
