from .is_development import IS_DEVELOPMENT


if IS_DEVELOPMENT:
    SERVER = 'dev'
else:
    SERVER = 'prod'
