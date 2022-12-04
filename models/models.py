# -*- coding: utf-8 -*-
from odoo import models, fields, api
#Diferencia entre dos fechas
from dateutil.relativedelta import *
#Saber la fecha actual
from datetime import date

class Subject(models.Model):
    _name = 'school.subject'
    _description ='permite ver el subject'
    _order = 'name'

    name = fields.Char('Name', required=True)
    credits = fields.Integer(string='Creditos', required=True)
    max_students = fields.Integer(string='Cantidad máxima de estudiantes', required=True)
    active = fields.Boolean(string='Activado', default=True)

    # Relations
    student_ids = fields.Many2many('school.student', string='Estudiantes')
    teacher_id = fields.Many2one('school.teacher', string='Profesores')

class Student(models.Model):
    _name ='school.student'
    _description = 'permite modificar estudiante'
    _order = 'name'

    name = fields.Char('Nombre de Alumno', required=True)
    birth_date = fields.Date(required=True)

    # Store no es necesario porque los datos varian al pasar del tiempo
    age = fields.Integer(string='Edad', compute='_get_age')
    final_exam_grade = fields.Float('Nota', (4,2), default=0.0, max=20.0, min=0.0)

    # Relations to father
    subject_ids = fields.Many2many('school.subject', string='Subject')

    @api.depends('birth_date')
    def _get_age(self):
        for student in self:
            today = date.today()
            student.age = relativedelta(today, student.birth_date).years

    # @api.depends('final_exam_grade')
    # def _validate(self):
    #     for student_note in self:
    #         if str(student_note.final_exam_grade) > 0 and str(student_note.final_exam_grade) < 21:
    #             student_note.final_exam_grade = student_note.final_exam_grade
    #         else:
    #             raise UserError("La nota no puede ser menor a 0 o superior a 20")



class Teacher(models.Model):
    _name = 'school.teacher'
    _description = 'permite modificar profesor'
    _order = 'name'

    name = fields.Char('Nombre de Profesor', required=True)
    profile = fields.Text('Perfil del profesor')

    subject_ids = fields.One2many('school.subject', 'teacher_id', string='Subject')
