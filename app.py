from shweb.services.rest import create_app


application = create_app()

if __name__ == "__main__":
    application.run(debug=True, load_dotenv=True)
