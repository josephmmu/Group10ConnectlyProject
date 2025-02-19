class UserRoleFactory:
    # Factory class for creating user role instances

    @staticmethod
    def get_role(user):
        if user.is_staff:
            return "Admin"
        elif user.groups.filter(name="Editor").exist():
            return "Editor"
        else:
            return "Regualr User"