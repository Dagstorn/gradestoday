from django.contrib import admin
from .models import Teacher, Group, Student, Comment


admin.site.site_header = "GRADES - todayschool.kz"
admin.site.site_title = "GRADES - todayschool.kz"


# teacher admin
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name','lastname','phone', 'subject', 'status')
    list_editable = ('status',)

# group admin
class GroupStudentInstanceInline(admin.TabularInline):
    model = Student
    extra = 1

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [GroupStudentInstanceInline]


#student admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name','lastname','group', 'unique_code')
    fields = ('name','lastname','group')


# comment admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('title','date','student', 'teacher' )




