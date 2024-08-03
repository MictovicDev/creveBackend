from django.db import models



# Blog:

# 1. Title
# 2. Description
# 3. Author
# 4. Date
# 5. Category

class Blog(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    author = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    cat

