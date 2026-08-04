"""
==================================================
YPTSC IMS
FLASK APPLICATION STARTUP
Enterprise v1
==================================================
"""


from app import create_app





# ==================================
# CREATE APPLICATION INSTANCE
# ==================================


app = create_app()







# ==================================
# APPLICATION RUNNER
# ==================================


if __name__ == "__main__":



    app.run(


        host="0.0.0.0",


        port=5000,


        debug=True



    )