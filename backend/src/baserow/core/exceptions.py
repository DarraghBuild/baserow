from django.db import OperationalError


class PermissionException(Exception):
    """
    Every permission related exception should inherit from this one.
    """


class IsNotAdminError(PermissionException):
    """
    Raised when the user tries to perform an action that is not allowed because he
    does not have admin permissions.
    """


class UserNotInGroup(PermissionException):
    """Raised when the user doesn't have access to the related group."""

    def __init__(self, user=None, group=None, *args, **kwargs):
        if user and group:
            super().__init__(
                f"User {user} doesn't belong to group {group}.", *args, **kwargs
            )
        else:
            super().__init__("The user doesn't belong to the group", *args, **kwargs)


class UserInvalidGroupPermissionsError(PermissionException):
    """Raised when a user doesn't have the right permissions to the related group."""

    def __init__(self, user, group, permissions, *args, **kwargs):
        self.user = user
        self.group = group
        self.permissions = permissions
        super().__init__(
            f"The user {user} doesn't have the right permissions {permissions} to "
            f"{group}.",
            *args,
            **kwargs,
        )

class ModifySuperAdminError(Exception):
    """Raised when a user tries to modify permissions for a super admin user."""

    def __init__(self, email, *args, **kwargs):
        self.email = email
        super().__init__(f"The user {email} is a super admin and cannot be modified.", *args, **kwargs)

class PermissionDenied(PermissionException):
    """
    Generic permission exception when a user doesn't have the right permissions to do
    the given operations.
    """

    def __init__(self, actor=None, *args, **kwargs):
        if actor:
            super().__init__(
                f"{actor} doesn't have the required permissions.", *args, **kwargs
            )
        else:
            super().__init__(f"Permission denied.", *args, **kwargs)


class GroupDoesNotExist(Exception):
    """Raised when trying to get a group that does not exist."""


class GroupUserDoesNotExist(Exception):
    """Raised when trying to get a group user that does not exist."""


class GroupUserAlreadyExists(Exception):
    """
    Raised when trying to create a group user that already exists. This could also be
    raised when an invitation is created for a user that is already part of the group.
    """


class GroupUserIsLastAdmin(Exception):
    """
    Raised when the last admin of the group tries to leave it. This will leave the
    group in a state where no one has control over it. He either needs to delete the
    group or make someone else admin.
    """


class CannotDeleteYourselfFromGroup(Exception):
    """
    Raised when the user tries to delete himself from the group. The `leave_group`
    method must be used in that case.
    """


class ApplicationDoesNotExist(Exception):
    """Raised when trying to get an application that does not exist."""


class ApplicationNotInGroup(Exception):
    """Raised when a provided application does not belong to a group."""

    def __init__(self, application_id=None, *args, **kwargs):
        self.application_id = application_id
        super().__init__(
            f"The application {application_id} does not belong to the group.",
            *args,
            **kwargs,
        )


class InstanceTypeAlreadyRegistered(Exception):
    """
    Raised when the instance model instance is already registered in the registry.
    """


class InstanceTypeDoesNotExist(Exception):
    """
    Raised when a requested instance model instance isn't registered in the registry.
    """

    def __init__(self, type_name, *args, **kwargs):
        self.type_name = type_name
        super().__init__(*args, **kwargs)


class ApplicationTypeAlreadyRegistered(InstanceTypeAlreadyRegistered):
    pass


class ApplicationTypeDoesNotExist(InstanceTypeDoesNotExist):
    pass


class ApplicationOperationNotSupported(Exception):
    """
    Raised when the particular operation is not supported by the
    application type.
    """


class AuthenticationProviderTypeAlreadyRegistered(InstanceTypeAlreadyRegistered):
    pass


class AuthenticationProviderTypeDoesNotExist(InstanceTypeDoesNotExist):
    pass


class PermissionManagerTypeAlreadyRegistered(InstanceTypeAlreadyRegistered):
    pass


class PermissionManagerTypeDoesNotExist(InstanceTypeDoesNotExist):
    pass


class ObjectScopeTypeAlreadyRegistered(InstanceTypeAlreadyRegistered):
    pass


class ObjectScopeTypeDoesNotExist(InstanceTypeDoesNotExist):
    pass


class OperationTypeAlreadyRegistered(InstanceTypeAlreadyRegistered):
    pass


class OperationTypeDoesNotExist(InstanceTypeDoesNotExist):
    pass


class SubjectTypeNotExist(Exception):
    """Raised when trying to use a subject type that does not exist."""


class BaseURLHostnameNotAllowed(Exception):
    """
    Raised when the provided base url is not allowed when requesting a password
    reset email.
    """


class GroupInvitationDoesNotExist(Exception):
    """
    Raised when the requested group invitation doesn't exist.
    """


class GroupInvitationEmailMismatch(Exception):
    """
    Raised when the group invitation email is not the expected email address.
    """


class TemplateDoesNotExist(Exception):
    """
    Raised when the requested template does not exist in the database.
    """


class TemplateFileDoesNotExist(Exception):
    """
    Raised when the JSON template file does not exist in the
    APPLICATION_TEMPLATE_DIRS directory.
    """


class TrashItemDoesNotExist(Exception):
    """
    Raised when the trash item does not exist in the database.
    """


class LockConflict(Exception):
    """
    Generic base class used for exceptions raised when an operation fails as part of
    Baserow has been locked for some operation.
    """


class InvalidPermissionContext(Exception):
    """
    Used when an invalid context is passed to a permission checker.
    """


class MaxLocksPerTransactionExceededException(Exception):
    """
    Baserow can sometimes perform operations that require a Postgres LOCK on a large
    number of tuples. If this quantity results in the lock count exceeding the value
    set in `max_locks_per_transaction`, a subclass of this exception will be raised.
    """

    message = (
        "Baserow has exceeded the maximum number of PostgreSQL locks per transaction. "
        "Please read https://baserow.io/docs/technical/postgresql-locks"
    )


def is_max_lock_exceeded_exception(exception: OperationalError) -> bool:
    """
    Returns whether the `OperationalError` which we've been given
    is due to `max_locks_per_transaction` being exceeded.
    """

    return "You might need to increase max_locks_per_transaction" in exception.args[0]


class DuplicateApplicationMaxLocksExceededException(
    MaxLocksPerTransactionExceededException
):
    """
    If someone tries to duplicate an application with a lot of tables in a single
    transaction, it'll quickly exceed the `max_locks_per_transaction` value set
    in Postgres. This exception is raised when we detect the scenario.
    """

    message = (
        "Baserow attempted to duplicate an application, but exceeded the maximum "
        "number of PostgreSQL locks per transaction. Please read "
        "https://baserow.io/docs/technical/postgresql-locks"
    )


class LastAdminOfGroup(Exception):
    """
    Raised when somebody tries to remove the last admin of a group.
    """


class IdDoesNotExist(Exception):
    """
    Raised when an ID is queried that does not exist
    """

    def __init__(self, not_existing_id=None, *args, **kwargs):
        self.not_existing_id = not_existing_id
        super().__init__(
            f"The id {not_existing_id} does not exist.",
            *args,
            **kwargs,
        )
