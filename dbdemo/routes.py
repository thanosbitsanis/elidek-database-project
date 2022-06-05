from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from dbdemo import app, db ## initially created by __init__.py, need to be used here
from dbdemo.forms import MyForm, FieldForm, Field3, ProjectForm

@app.route("/",methods=["GET","POST"])
def index():
    form = FieldForm()
    if request.method=="POST" and form.validate_on_submit():

        field=form.__dict__
        x=field["field"].data
        return redirect(url_for("getFieldss",fields=x))
    else:
        try:
            ## create connection to database
            cur = db.connection.cursor()
            cur2= db.connection.cursor()
            ## execute query
            cur.execute("SELECT * from telephones")
            ## cursor.fetchone() does not return the column names, only the row values
            ## thus we manually create a mapping between the two, the dictionary res
            #column_names = [i[0] for i in cur.description]
            #res = dict(zip(column_names, cur.fetchone()))
            #best_dribbling_grade = res.get("grade")
            #best_dribbler = res.get("name") + " " + res.get("surname")
            column_names = [i[0] for i in cur.description]
            telephones = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    
            #cur.execute("SELECT g.grade, s.name, s.surname FROM students s INNER JOIN grades g ON g.student_id = s.id WHERE g.course_name = 'SHO' ORDER BY g.grade DESC LIMIT 1")
            #res = dict(zip(column_names, cur.fetchone()))
        
            cur.close()
            #best_shooting_grade = res.get("grade")
            #best_shooter = res.get("name") + " " + res.get("surname")

            return render_template("base.html",telephones=telephones, pageTitle = "ELIDEK",form = form)
            #                      
        except Exception as e:
            print(e)
            return render_template("base.html", pageTitle = "ELIDEK",form = form)


@app.route("/3.1.programs")
def getPrograms():
        
        try:
            tablename1 = "-TABLE : All Programs"
            
            cur = db.connection.cursor()
            cur.execute("SELECT * FROM Elidek_program")
            column_names=[i[0] for i in cur.description]
            view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            #form = StudentForm()
            
            #cur.execute("SELECT * FROM students")
            #column_names = [i[0] for i in cur.description]
            #students = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            
            return render_template("programs.html", view1 = view1, table1 = tablename1, pageTitle = "ALL PROGRAMS") #pageTitle = "Students Page"
                                                                
        except Exception as e:
            ## if the connection to the database fails, return HTTP response 500
            flash(str(e), "danger")
            abort(500)


@app.route("/3.1.projects",methods=["GET","POST"])
def getProjects():
   
    form = Field3()
    if request.method=="POST" and form.validate_on_submit():

        field=form.__dict__
        date=field["date"].data
        duration = field["duration"].data
        staff = field["staff"].data
        
        try:
            tablename1 = "-TABLE : All Projects"
            
            cur = db.connection.cursor()

            if date != "" and duration != "" and staff != "":
                cur.execute("SELECT project_title, org_name FROM Project WHERE project_start < '{}' AND project_end > '{}' AND duration = '{}' AND staff_id = '{}' ".format(date, date, duration, staff))
                column_names=[i[0] for i in cur.description]
                view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]

            elif date != "" and duration != "" and staff == "":
                cur.execute("SELECT project_title, org_name FROM Project WHERE project_start < '{}' AND project_end > '{}' AND duration = '{}' ".format(date, date, duration))
                column_names=[i[0] for i in cur.description]
                view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]

            elif date != "" and duration == "" and staff != "":
                cur.execute("SELECT project_title, org_name FROM Project WHERE project_start < '{}' AND project_end > '{}' AND staff_id = '{}' ".format(date, date, staff))
                column_names=[i[0] for i in cur.description]
                view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]

            elif date == "" and duration != "" and staff != "":
                cur.execute("SELECT project_title, org_name FROM Project WHERE duration = '{}' AND staff_id = '{}' ".format(duration, staff))
                column_names=[i[0] for i in cur.description]
                view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]

            elif date != "" and duration == "" and staff == "":
                cur.execute("SELECT project_title, org_name FROM Project WHERE project_start < '{}' AND project_end > '{}' ".format(date, date))
                column_names=[i[0] for i in cur.description]
                view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]

            elif date == "" and duration != "" and staff == "":
                cur.execute("SELECT project_title, org_name FROM Project WHERE duration = '{}' ".format(duration))
                column_names=[i[0] for i in cur.description]
                view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]

            elif date == "" and duration == "" and staff != "":
                cur.execute("SELECT Project_title, org_name FROM Project WHERE staff_id = '{}' ".format(staff))
                column_names=[i[0] for i in cur.description]
                view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]

            cur.close()

            return render_template("projects.html",view1 = view1,table1 = tablename1, pageTitle = "ALL PROJECTS", form = form)


        except Exception as e:
            ## if the connection to the database fails, return HTTP response 500
            flash(str(e), "danger")
            abort(500)

    else:    
        try:
            tablename1 = "-TABLE : All Projects"
            
            cur = db.connection.cursor()
            cur.execute("SELECT project_title, org_name FROM Project")
            column_names=[i[0] for i in cur.description]
            view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            #form = StudentForm()
            
            #cur.execute("SELECT * FROM students")
            #column_names = [i[0] for i in cur.description]
            #students = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            
            return render_template("projects.html", view1 = view1, table1 = tablename1, pageTitle = "ALL PROJECTS", form = form) #pageTitle = "Students Page"
                                                                
        except Exception as e:
            ## if the connection to the database fails, return HTTP response 500
            flash(str(e), "danger")
            abort(500)


@app.route("/3.1.projects.researchers",methods=["GET","POST"])
def getProjectsResearchers():
    form = ProjectForm()
    tablename1 = "-TABLE : Project's researchers"
    if request.method=="POST" and form.validate_on_submit():

        field=form.__dict__
        x=field["field"].data
        try:
            cur = db.connection.cursor()
            cur.execute("SELECT researcher_name, researcher_lastname, researcher_id from researcher where researcher_id in (select researcher_id from works_for where project_title = '{}') ".format(x))
            column_names=[i[0] for i in cur.description]
            view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]

            cur.close()   
            #form = StudentForm()
            
            #cur.execute("SELECT * FROM students")
            #column_names = [i[0] for i in cur.description]
            #students = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            
            return render_template("projectresearchers.html", view1 = view1, table1 = tablename1 ,pageTitle = "PROJECT'S RESEARCHERS", form=form) #pageTitle = "Students Page"
                                                            
        except Exception as e:
            ## if the connection to the database fails, return HTTP response 500
            flash(str(e), "danger")
            abort(500)

    return render_template("projectresearchers.html", view1 = [], table1 = tablename1 ,pageTitle = "PROJECT'S RESEARCHERS",form = form)


@app.route("/3.2.view1")
def getView1():
   
    #Retrieve students from database
    
    try:
        tablename1 = "-TABLE : Researcher_projects"
        cur = db.connection.cursor()
        cur.execute("CREATE VIEW researcher_projects AS SELECT Researcher.researcher_name, Researcher.researcher_lastname, Researcher.researcher_id, Works_for.project_title FROM Researcher, Works_for WHERE Researcher.researcher_id = Works_for.researcher_id")
        cur.execute("SELECT * FROM researcher_projects ORDER BY researcher_name")
        column_names=[i[0] for i in cur.description]
        view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]
        
        cur.execute("DROP VIEW researcher_projects")
        cur.close()   
        #form = StudentForm()
        
        #cur.execute("SELECT * FROM students")
        #column_names = [i[0] for i in cur.description]
        #students = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        
        return render_template("view1.html", view1 = view1, table1 = tablename1, pageTitle = "VIEW 1") #pageTitle = "Students Page"
                                                            
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/3.2.view2")
def getView2():
   
    #Retrieve students from database
    
    try:
        tablename1 = "-TABLE : Project_overview"

        cur = db.connection.cursor()
        cur.execute("CREATE VIEW project_overview AS SELECT Project.project_title,Project.project_budget, Evaluation.evaluation_grade,Project.researcher_id FROM Project, Evaluation WHERE Project.evaluation_id=Evaluation.evaluation_id ")
        cur.execute("SELECT * FROM project_overview ORDER BY evaluation_grade DESC")
        column_names=[i[0] for i in cur.description]
        print (column_names)
        view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]
            
        cur.execute("DROP VIEW project_overview") 
        cur.close()
                #form = StudentForm()
                
                #cur.execute("SELECT * FROM students")
                #column_names = [i[0] for i in cur.description]
                #students = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
                
        return render_template("view2.html", view1 = view1, table1 = tablename1, pageTitle = "VIEW 2") #pageTitle = "Students Page"
                                                                    
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/3.3-<fields>")
def getFieldss(fields):


        
        try:
            query="SELECT * FROM Works_for WHERE Project_title IN (SELECT Project_title FROM Project WHERE (project_start < DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND project_end > CURDATE() ) AND Project_title IN (SELECT project_title FROM Field_of_project WHERE (field_name='{}')))".format(fields)
            tablename1=fields
            ## create connection to database
            cur = db.connection.cursor()
            ## execute query
            cur.execute(query)

            column_names = [i[0] for i in cur.description]
            table = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()

            return render_template("fields.html",table1=tablename1,view1=table,pageTitle="SCIENTIFIC FIELD PROJECTS")
             #
        except Exception as e:
            print(e)
            return render_template("base.html", pageTitle = "ELIDEK",form = form)


@app.route("/3.4")
def getEqual():
   
    #Retrieve students from database
    
    try:
        tablename1 = "-TABLE : EQUAL PROJECTS"
        
        cur = db.connection.cursor()
        cur.execute("CREATE VIEW num_of_proj as SELECT EXTRACT(YEAR from project.project_start) as years, organization.org_name as organization_title, count(project.project_title) as num_of_proj FROM manages,organization,project WHERE organization.org_name = manages.org_name AND project.project_title = manages.project_title GROUP BY years, organization_title;")
        cur.execute("SELECT organization.org_name FROM organization,(SELECT table1.organization_title, table1.num_of_proj FROM num_of_proj as table1, num_of_proj as table2 WHERE (table1.organization_title = table2.organization_title AND table1.num_of_proj = table2.num_of_proj AND table1.years - table2.years = 1)) as newtable WHERE (organization_title = organization.org_name AND num_of_proj>=10);")
        column_names=[i[0] for i in cur.description]
        view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.execute("DROP VIEW num_of_proj")
        cur.close()
        #form = StudentForm()
        
        #cur.execute("SELECT * FROM students")
        #column_names = [i[0] for i in cur.description]
        #students = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        
        return render_template("equal_projects.html", view1 = view1, table1 = tablename1, pageTitle = "EQUAL PROJECTS FOR THE SAME ORGANIZATION IN CONSECUTIVE YEARS") #pageTitle = "Students Page"
                                                            
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)



@app.route("/3.5")
def getFields():
   
    #Retrieve students from database
    
    try:
        tablename1 = "-TABLE : Pairs"
        
        cur = db.connection.cursor()
        cur.execute("CREATE VIEW Pairs AS SELECT c.field_name AS Field1, a.field_name AS Field2 FROM field_of_project c, field_of_project a WHERE (a.field_name > c.field_name AND c.project_title IN (SELECT Project_title FROM Project) AND  a.project_title IN (SELECT Project_title FROM Project) AND a.project_title=c.project_title);")
        cur.execute("SELECT Field1, Field2, COUNT(*) AS Appearance_count FROM Pairs GROUP BY Field1, Field2 ORDER BY Appearance_count DESC LIMIT 3;")
        column_names=[i[0] for i in cur.description]
        view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.execute("DROP VIEW Pairs")
        cur.close()
        #form = StudentForm()
        
        #cur.execute("SELECT * FROM students")
        #column_names = [i[0] for i in cur.description]
        #students = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        
        return render_template("pairs.html", view1 = view1, table1 = tablename1, pageTitle = "PAIRS") #pageTitle = "Students Page"
                                                            
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/3.6")
def getWorkers():
   
    #Retrieve students from database
    
    try:
        tablename1 = "-TABLE : Best_young_researchers"
        
        cur = db.connection.cursor()
        cur.execute("CREATE VIEW active_workers AS SELECT researcher_id AS id FROM Works_for WHERE researcher_id IN (SELECT researcher_id FROM Works_for WHERE project_title IN (SELECT project_title FROM Project WHERE (project_start < CURDATE() AND project_end > CURDATE())));")
        cur.execute("CREATE VIEW active_researchers AS SELECT Researcher.researcher_name, Researcher.researcher_lastname, active_workers.id FROM Researcher INNER JOIN active_workers ON Researcher.researcher_id=active_workers.id;")
        cur.execute("SELECT *, COUNT(*) AS spots_in_projects FROM active_researchers WHERE id IN (SELECT researcher_id FROM Researcher WHERE (TIMESTAMPDIFF(YEAR, researcher_birthdate,CURDATE()) < 40)) GROUP BY id ORDER BY spots_in_projects DESC LIMIT 5;")
        column_names=[i[0] for i in cur.description]
        view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.execute("DROP VIEW active_workers")
        cur.execute("DROP VIEW active_researchers")
        cur.close()
        #form = StudentForm()
        
        #cur.execute("SELECT * FROM students")
        #column_names = [i[0] for i in cur.description]
        #students = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        
        return render_template("best_young_researchers.html", view1 = view1, table1 = tablename1, pageTitle = "BEST_YOUNG_RESEARCHERS") #pageTitle = "Students Page"
                                                            
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/3.7")
def getStaff():
   
    #Retrieve students from database
    
    try:
        tablename1 = "-TABLE : Best_staff"
        
        cur = db.connection.cursor()
        cur.execute("CREATE VIEW best_staff AS  SELECT staff.staff_name as staff, staff.staff_id as id, project.org_name as company_name, project.project_budget as budget FROM Staff INNER JOIN project ON staff.staff_id = project.staff_id WHERE project.org_name IN (SELECT org_name FROM company) ORDER BY project.project_budget DESC;")
        cur.execute("SELECT staff, company_name, SUM(budget) as total_funds FROM best_staff GROUP BY id ORDER BY total_funds DESC LIMIT 5;")
        column_names=[i[0] for i in cur.description]
        view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.execute("DROP VIEW best_staff")
        cur.close()
        #form = StudentForm()
        
        #cur.execute("SELECT * FROM students")
        #column_names = [i[0] for i in cur.description]
        #students = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        
        return render_template("best_staff.html", view1 = view1, table1 = tablename1, pageTitle = "BEST_STAFF") #pageTitle = "Students Page"
                                                            
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/3.8")
def getResearcher():
   
    #Retrieve students from database
    
    try:
        tablename1 = "-TABLE : Workers in projects without deliverables"
        
        cur = db.connection.cursor()
        cur.execute("create VIEW workers_no_deliverables as (select RESEARCHER_ID from works_for where project_title in (SELECT t1.project_title FROM project t1 LEFT JOIN deliverables t2 ON t2.project_title = t1.project_title WHERE t2.project_title IS NULL));")
        cur.execute("SELECT r.researcher_name, r.researcher_lastname, COUNT(w.researcher_id) as number_of_project_no_deliverables FROM  researcher r INNER JOIN workers_no_deliverables w ON w.researcher_id = r.researcher_id  GROUP BY w.researcher_id HAVING number_of_project_no_deliverables >= 5 ORDER BY number_of_project_no_deliverables DESC;")
        column_names=[i[0] for i in cur.description]
        view1=[dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.execute("DROP VIEW workers_no_deliverables")
        cur.close()
        #form = StudentForm()
        
        #cur.execute("SELECT * FROM students")
        #column_names = [i[0] for i in cur.description]
        #students = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        
        return render_template("no_deliverables.html", view1 = view1, table1 = tablename1, pageTitle = "WORKERS IN PROJECTS WITHOUT DELIVERABLES") #pageTitle = "Students Page"
                                                            
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)        