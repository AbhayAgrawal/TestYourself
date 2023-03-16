from django.db import models

# Create your models here.
class QuizMst(models.Model):
    qid = models.AutoField(db_column='QID', primary_key=True)  # Field name made lowercase.
    qname = models.TextField(db_column='QNAME')  # Field name made lowercase.
    op1 = models.TextField(db_column='OP1')  # Field name made lowercase.
    op2 = models.TextField(db_column='OP2')  # Field name made lowercase.
    op3 = models.TextField(db_column='OP3')  # Field name made lowercase.
    correct_op = models.CharField(db_column='CORRECT_OP', max_length=3)  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'quiz_mst'

class StudentMst(models.Model):
    sid = models.AutoField(db_column='SID', primary_key=True)  # Field name made lowercase.
    student_name = models.CharField(db_column='STUDENT_NAME', max_length=90)  # Field name made lowercase.
    correct_ans = models.IntegerField(db_column='CORRECT_ANS')  # Field name made lowercase.
    wrong_ans = models.IntegerField(db_column='WRONG_ANS')  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=45)  # Field name made lowercase.
    total_marks = models.IntegerField(db_column='TOTAL_MARKS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'student_mst'

# Create your models here.
