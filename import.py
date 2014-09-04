from flask import Flask, request, jsonify, g
from flask.ext.sqlalchemy import SQLAlchemy
import pyPdf
import goslate
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/bron'
db = SQLAlchemy(app)


class Pages(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.Text)
	page_id = db.Column(db.Integer)
	book_id = db.Column(db.Integer)
	translation = db.Column(db.Text)
	translated = db.Column(db.Integer)


	def translate(self):
		self.translation = goslate.Goslate().translate(self.body, 'en')
		self.translated = 1

	def __init__(self, body, page_id, book_id):
		self.body = body
		self.page_id = page_id
		self.book_id = book_id
		self.translate()

	def save(self):
		db.session.add(self)
		db.session.commit()



pdf = pyPdf.PdfFileReader(open("Book1.pdf", "rb"))
for i in range(0, len(pdf.pages)):
	print "1 - " + str(i)
	p = Pages(pdf.getPage(i).extractText(), i + 1, 1)
	p.save()
	time.sleep(1) #to get around api limits


pdf = pyPdf.PdfFileReader(open("book2-small.pdf", "rb"))
for i in range(174, 185):
	print "2 - " + str(i)
	page = Pages(pdf.getPage(i).extractText(), i + 1, 2)
	page.save()
	time.sleep(1)


# cleanup

for page in Pages.query.all():
	page.translation = page.translation.replace("Source", "Bron")
	page.save()


# drop database bron;
# create database bron;
# create table bron.pages (id INT(4) NULL AUTO_INCREMENT, page_id INTEGER(4), book_id INTEGER(4), body TEXT, translation TEXT, translated VARCHAR(1), PRIMARY KEY (id));
