import shweb

if __name__ == "__main__":
    shweb.app.run(debug=True, port=shweb.env.config.port)
