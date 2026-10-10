import logging

from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            print("I'm in the validator")
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Please enter a  valid email address"))

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        else:
            email = self.normalize_email(email)
            self.email_validator(email)
            
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        
        # If department is provided but school is not, infer school from department
        dept = extra_fields.get("department")
        if dept and not extra_fields.get("school"):
            try:
                extra_fields["school"] = dept.school
            except AttributeError as exc:
                logger.debug("Could not infer school from department: %s", exc)

        # If school is provided but university is not, infer university from school
        sch = extra_fields.get("school")
        if sch and not extra_fields.get("university"):
            try:
                extra_fields["university"] = sch.university
            except AttributeError as exc:
                logger.debug("Could not infer university from school: %s", exc)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser set to True")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff set to True")
        #if extra_fields.get("is_verified") is not True:
            #raise ValueError("Superuser must have is_verified set to True")
        user = self.create_user(email, password, **extra_fields)
        return user
