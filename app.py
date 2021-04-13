import shweb

application = shweb.app

if __name__ == "__main__":
    application.run(debug=True, host=shweb.env.config.host, port=shweb.env.config.port)
