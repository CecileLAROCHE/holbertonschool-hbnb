from app import create_app

# Crée l'application avec la configuration de développement
app = create_app('development')
# charge DevelopmentConfig depuis le dict config

if __name__ == '__main__':
    app.run(debug=True)
