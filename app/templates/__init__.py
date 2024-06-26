# *NO* idea if this layout is actually good or encouraged -
# but I couldn't put this instantiation in `app.__init__.py` or
# `app.routers.__init__.py` and then import from there into (say)
# `app.routers.decks.py` because:
#
# ImportError: cannot import name 'jinja_templates' from partially initialized module 'app.routers' (most likely due to a circular import) (/Users/scubbo/Code/edh-elo/app/routers/__init__.py)

from json import dumps

from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

jinja_templates = Jinja2Templates(directory="app/templates")


# TODO - would this be better as a method on a class extending `db.Model` that the classes in `models.py` could then
# extend?
# (Probably not, as we'd still need to explicitly call it - it wouldn't be implicitly called _by_ Flask)
#
# (Assumes that this will only be passed lists or objects, not primitives)
# def _jsonify(o):
#     if hasattr(o, "__dict__"):
#         return {k: v for (k, v) in o.__dict__.items() if k != "_sa_instance_state"}
#     else:
#         return [_jsonify(e) for e in o]


# https://fastapi.tiangolo.com/tutorial/encoder/
def _jsonify(o):
    return dumps(jsonable_encoder(o))
