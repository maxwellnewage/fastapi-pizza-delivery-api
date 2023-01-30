from globals import engine, Base

Base.metadata.create_all(bind=engine)
