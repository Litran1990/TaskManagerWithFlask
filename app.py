import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
# We also said that MongoDB stores its data in a JSON like format called BSON.
# So our edit_task() function receives the task ID as part of its routing parameter.
# And in order to work with this parameter and find a match in MongoDB, we must convert that to a BSON data type.
from bson.objectid import ObjectId

# We also need to install a package called dnsython to use the new style connection string for MongoDB Atlas.

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb+srv://Litran1990:Palmeiras1999@myfirstcluster-fu8x1.mongodb.net/task_manager?retryWrites=true'

# Now that that's done, let's create an instance of PyMongo
mongo = PyMongo(app)

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("index.html", tasks=mongo.db.tasks.find())


@app.route('/add_task')
def add_task():
    return render_template("addtask.html", categories=mongo.db.categories.find())
    
@app.route('/insert_task', methods=["POST"])
def insert_task():
    tasks = mongo.db.tasks
    # Remember, whenever you submit information to a URI or to some web location, it is submitted in the form of a request object.
    tasks.insert_one(request.form.to_dict())
    # Once that's done, we redirect to get_tasks, so we can view that new task in our collection.
    return redirect(url_for('get_tasks'))
    
    
@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('edittask.html', task=the_task,
                           categories=all_categories)
                           
                           
@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'task_name':request.form.get('task_name'),
        'category_name':request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))
    
    
@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


@app.route('/get_categories')
def get_categories():
    return render_template('categories.html', categories=mongo.db.categories.find())
    

@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
                           category=mongo.db.categories.find_one(
                           {'_id': ObjectId(category_id)}))


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))
    
    
@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))
    

@app.route('/insert_category', methods=['POST'])
def insert_category():
    category_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))


@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')
        

"""Set up our IP address and our port number so that Cloud9 knows how to run and where to run our application"""
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=int(os.environ.get('PORT')), debug=False)
    