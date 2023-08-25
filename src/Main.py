import hupper
import app  

if __name__ == "__main__":
    reloader = hupper.start_reloader('app.main')
    app.main()
    
