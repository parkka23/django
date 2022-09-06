from django.contrib import admin
from groups.models import Teacher, Student, Group,GroupStudents
# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(GroupStudents)
# admin.site.register(Group)

@admin.register(Group)
class Groups(admin.ModelAdmin):
    list_display=('id','title','teacher_id','count_of_students','list_of_students')

    def list_of_students(self,obj):
        # print(obj.id,'----------------------------------------') #germ-12
        # query set - вытаскивать из бд
        # qs=GroupStudents.objects.all()
        qs=GroupStudents.objects.filter(group_id=obj.id)
        # print(qs,'111111111111111111111') 
        res=[]
        for x in qs:
            # print(x)
            # print(type(x))
            x=str(x).split(' ')
            x=x[0]+' '+x[1]
            res.append(x)
        if not res: return 'No students'
        else: return res

    def count_of_students(self,obj):
        qs=GroupStudents.objects.filter(group_id=obj.id)
        # qs=GroupStudents.objects.filter(group_id=obj.id).values() all fields
        return  qs.count()
