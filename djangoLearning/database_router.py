class DatabaseRouter:
    """
    A router to control all database operations on models in the product app.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'products':
            return 'productdb'  
        return None  

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'products':
            return 'productdb'  
        return None  

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'products'  and obj2._meta.app_label == 'products':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'products':
            return db == 'productdb'  
        return db == 'default'  
