from django.db import models



# Blog:

# 1. Title
# 2. Description
# 3. Author
# 4. Date
# 5. Category

class Category(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    author = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='files/images', blank=True, null=True)

    def __str__(self):
        return self.title
    

