import motor.motor_asyncio


cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://kozlobogdann:NRBHiJcL5uHvDAEI@cluster0.npttskr.mongodb.net/?retryWrites=true&w=majority")

musicians = cluster.Help_Musician_DB.user
events = cluster.Help_Musician_DB.events
