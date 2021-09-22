from flask import request, render_template
import app
@app.errorhandler(404)
def page_not_found(e):

    app.logger.info(f"Page not found: {request.url}")

    return render_template("404.html")
