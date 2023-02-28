from piazzabot.piazzabot import app_handler, logger, dbengine, cache
from piazzabot.database import Course

from fastapi import FastAPI, Request, status
from sqlalchemy.orm import Session

api = FastAPI()


@api.on_event("startup")
async def startup_event():
    with Session(dbengine) as session:
        courses = session.query(Course)
        for course in courses:
            cache[course.workspace] = course.forum

    logger.info("cache built:")
    logger.info(cache)


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)


@api.get("/slack/install")
async def install(req: Request):
    return await app_handler.handle(req)


@api.get("/slack/oauth_redirect")
async def oauth_redirect(req: Request):
    return await app_handler.handle(req)


@api.on_event("shutdown")
def shutdown_event():
    logger.info("Shutting down PiazzaBot...")
    with Session(dbengine) as session:
        for workspace in cache:
            course = Course(workspace=workspace, forum=cache[workspace])
            session.merge(course)
        session.commit()

    logger.info("goodbye!")


@api.get('/healthcheck', status_code=status.HTTP_200_OK)
def perform_healthcheck():
    return {'healthcheck': 'Everything OK!'}
