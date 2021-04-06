import shweb

application = shweb.app

if __name__ == "__main__":
    application.run(debug=True, port=shweb.env.config.port)
