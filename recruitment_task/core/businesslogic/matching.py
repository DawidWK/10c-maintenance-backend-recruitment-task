from core.businesslogic.investing import invest_into_project
from core.businesslogic.errors import CannotInvestIntoProjectException

from core.models import Project

from django.db import models


def matching_logic(base_object: models.Model, matches_objects: models.Model) -> list:
    """returns list of objects that matches base object"""
    matches_list = []
    for object in matches_objects:
        try:
            if isinstance(base_object, Project):
                invest_into_project(object, base_object)
            else:
                invest_into_project(base_object, object)
        except CannotInvestIntoProjectException:
            pass
        else:
            matches_list.append(object.id)
    return matches_list
