import json
from flask import Flask, render_template, send_from_directory, request
from flask import jsonify, request, flash
from pymongo import MongoClient, ReturnDocument
import re
from datetime import datetime
import time

from forms import InsertForm
from updateForm import UpdateForm
from deleteForm import DeleteForm
from queryForm import QueryForm

from bson.objectid import ObjectId

client = MongoClient()
db = client.newAlphaTest
collection = db.testAlpha


app = Flask(__name__)
app.secret_key = 'development key'

@app.route("/")
def home():
    return send_from_directory("templates","home.html")

@app.route("/test", methods=['POST', 'GET'])
def test():
    form = QueryForm

    if request.method == 'POST':
        if form().validate() ==False:
            flash('All Fields are required!')
            return render_template("query.html", form = form())
        else:
            now = datetime.fromtimestamp(time.time())
            
            res = []
            myregex = re.compile(request.form["value"], re.I)
            for user in collection.find({request.form["key"]: myregex}):
        #res.append('<br/>')
        #res.append('<br/>')
                _tmp = user
                print _tmp
                print "\n"
        #        del(_tmp['_id'])
                res.append(_tmp)
                return render_template('table.html', result=res)
            print _tmp['_id'].getTimestamp()
            dummy_data = {"a1":11, "b1":222}
#            print "received this input: %s" % (user_input)
    #    collection.find().forEach(function(doc){ d = doc._id.getTimeStamp(); print(d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate())})
 #           return json.dumps(str(request.data))
    #    return json.dumps({})

        
    elif request.method == 'GET':
        return render_template("query.html", form = form())

@app.route("/query")
def query():
    return send_from_directory("static", "test.html")


@app.route("/insert", methods=['POST', 'GET'])
def insert():

    form = InsertForm

    if request.method == 'POST':
        if form().validate() ==False:
            flash('All Fields are required!')
            return render_template("insert.html", form = form())
        else:
            now = datetime.fromtimestamp(time.time())
            collection.insert({'process_name':request.form['process_name'],'cross_section':request.form['cross_section'],'total_uncertainty':request.form['total_uncertainty'],'other_uncertainty':request.form['other_uncertainty'],'cuts':request.form['cuts'],'kFactor':request.form['kFactor'],'reweighting':request.form['reweighting'],'shower':request.form['shower'],'matrix_generator':request.form['matrix_generator'],'contact':request.form['contact'],'DAS':request.form['DAS'],'MCM':request.form['MCM'],'refs':request.form['refs'],'accuracy':request.form['accuracy'],'valid':now.strftime('%Y-%m-%d')})
#'valid':request.form['valid'],'test':request.form['test']})

            
            writeFile = open("/afs/cern.ch/work/s/szaleski/app/Log.txt", "a")
            writeFile.write("\n\nThis is an insert operation!")
            writeFile.write("\n\n"+now.strftime('%H:%M:%S %Y-%m-%d'))
            writeFile.write("\nprocess_name:"+request.form['process_name'])
            writeFile.write("\ncross_section:"+request.form['cross_section'])
            writeFile.write("\naccuracy:"+request.form['accuracy'])
            writeFile.write("\ntotal_uncertainty:"+request.form['total_uncertainty'])
            writeFile.write("\nother_uncertainty:"+request.form['other_uncertainty'])
            writeFile.write("\ncuts:"+request.form['cuts'])
            writeFile.write("\nkFactor:"+request.form['kFactor'])
            writeFile.write("\nreweighting:"+request.form['reweighting'])
            writeFile.write("\nshower:"+request.form['shower'])
            writeFile.write("\nmatrix_generator:"+request.form['matrix_generator'])
            writeFile.write("\ncontact:"+request.form['contact'])
            writeFile.write("\nrefs:"+request.form['refs'])
            writeFile.write("\nDAS:"+request.form['DAS'])
            writeFile.write("\nMCM:"+request.form['MCM'])
            writeFile.close()
            return render_template("success.html")
        
    elif request.method == 'GET':
        return render_template("insert.html", form = form())

@app.route("/update", methods=['POST', 'GET'])
def update():
    form = UpdateForm
    if request.method == 'POST':
        if form().validate() == False:
            flash('Please fill in all Fields!')
            return render_template("update.html", form = form())
        else:
            now = datetime.fromtimestamp(time.time())
            collection.update({'_id':ObjectId(request.form['object_id'])},{'$set':{request.form['updateKey']:request.form['updateValue']}}, upsert=False)
            writeFile = open("/afs/cern.ch/work/s/szaleski/app/Log.txt", "a")
            writeFile.write("\n\nThis is an update operation!")
            writeFile.write("\n\n"+now.strftime('%H:%M:%S %Y-%m-%d'))
            writeFile.write("\nObjectId:"+request.form['object_id'])
            writeFile.write("\n"+request.form['updateKey']+":"+request.form['updateValue'])
            writeFile.close()
#            collection.update({'process_name':request.form['process_name']}, {'$set':{request.form['updateKey']:request.form['updateValue']}}, upsert=False)
            return render_template("success.html")
    elif request.method == 'GET':
        return render_template("update.html", form = form())

@app.route("/remove", methods=['POST', 'GET'])
def remove():
    form = DeleteForm
    if request.method == 'POST':
        if form().validate() == False:
            flash('Please fill in all Fields!')
            return render_template("delete.html", form = form())
        else:
            now = datetime.fromtimestamp(time.time())
            collection.delete_one({'_id':ObjectId(request.form['object_id'])})
            writeFile = open("/afs/cern.ch/work/s/szaleski/app/Log.txt", "a")
            writeFile.write("\n\nThis is an delete operation!")
            writeFile.write("\n\n"+now.strftime('%H:%M:%S %Y-%m-%d'))
            writeFile.write("\nObjectId:"+request.form['object_id'])
            writeFile.close()
#            collection.update({'process_name':request.form['process_name']}, {'$set':{request.form['updateKey']:request.form['updateValue']}}, upsert=False)
            return render_template("success.html")
    elif request.method == 'GET':
        return render_template("delete.html", form = form())


@app.route("/search", methods=['POST'])
def search():
    res = []
    search_value = json.loads(request.data)
    print "##DEBUG## DATA: %s search:%s" % (request.data, search_value) 
    myregex = re.compile(search_value['value'], re.I)
    for user in collection.find({search_value['key']: myregex}):#search_value['value'] }):
        #res.append('<br/>')
        #res.append('<br/>')
        _tmp = user
        print _tmp
        print "\n"
        del(_tmp['_id'])
        res.append(_tmp)
        print _tmp['process_name']

    return json.dumps(res, indent=4)



    print "received this input: %s" % (request.data)


    #return json.dumps(dummy_data)
#    return json.dumps(str(request.data))


@app.route('/search1/<key>/<user_input>', methods=['GET'])#{"key":"<key>","value":"<user_input>"}', methods=['GET'])
def search1(key, user_input):
    res = []
    myregex = re.compile(user_input, re.I)
    for user in collection.find({key: myregex}):
        #res.append('<br/>')
        #res.append('<br/>')
        _tmp = user
        print _tmp
        print "\n"
#        del(_tmp['_id'])
        res.append(_tmp)
    return render_template('table.html', result=res)
    print _tmp['_id'].getTimestamp()
    dummy_data = {"a1":11, "b1":222}
    print "received this input: %s" % (user_input)
#    collection.find().forEach(function(doc){ d = doc._id.getTimeStamp(); print(d.getFullYear()+"-"+(d.getMonth()+1)+"-"+d.getDate())})
    return json.dumps(str(request.data))
#    return json.dumps({})

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=4241)
