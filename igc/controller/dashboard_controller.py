from flask import redirect
from flask import request

from igc.controller import auth_controller
from igc.util import fileio
from igc.util.util import session_scope
from igc.util.cache import students, cacheStudentData

def controller(app, models, db):

    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta name="description" content="">
        <meta name="author" content="">
        <link rel="icon" href="favicon.ico">
    
        <title>Student Information System</title>
    
        <!-- Bootstrap core CSS -->
        <link href="../../static/bower_components/bootstrap/dist/css/bootstrap.min.css" rel="stylesheet">
    
    </head>
    
    <body>
    <div class="jumbotron">
        <div class="container">
            <h1 class="display-3">Dashboard</h1>
            <p>{full_name}</p>
            <button id="logout" class="btn btn-danger btn-lg">Logout</button>
        </div>
    </div>
    
    <div class="container">
        <div class="row">
            <table class="table table-hover table-bordered">
                <thead>
                    {table_headers}
                </thead>
                <tbody>
                    {table_body}
                </tbody>
            </table>
        </div>
    
        <hr>
    
        <footer>
            <p>&copy; VBCPS 2017</p>
        </footer>
    </div> <!-- /container -->
    
    
    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="../../static/bower_components/jquery/dist/jquery.min.js"></script>
    <script src="../../static/bower_components/bootstrap/dist/js/bootstrap.min.js"></script>
    <script src="../../static/bower_components/bootstrap-validator/dist/validator.min.js"></script>
    <link href="../../static/bower_components/toastr/toastr.min.css" rel="stylesheet">
    <script src="../../static/bower_components/toastr/toastr.min.js"></script>
    <script>
        $("#logout").click(function(e){
            location.pathname = "/index.html"
            location.search = ""
        });
    
    </script>
    </body>
    </html>
    """


    @app.route("/dashboard.html")
    def dashboard():
        User = models["user"]
        token = request.args.get('token')
        with session_scope(db) as session:
            user = session.query(User).filter(User.token == token).first()
            if user and int(user.student_id) in auth_controller.user_keys:
                string = template

                if students[user.student_id]["table_body"] is None:
                    cacheStudentData(user.student_id, students[user.student_id])

                cache = students[user.student_id]
                string = string.replace("{full_name}", cache["full_name"])
                string = string.replace("{table_headers}", cache["welcome_message"])
                string = string.replace("{table_body}", cache["table_body"])
                return string
            else:
                return redirect("index.html?reason=login", code=302)