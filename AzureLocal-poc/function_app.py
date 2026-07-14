import azure.functions as func

from poller import run_poller

app = func.FunctionApp()

@app.schedule(
    schedule="0 */5 * * * *",
    arg_name="timer",
    run_on_startup=False,
    use_monitor=True,
)
def poller(timer: func.TimerRequest):
    run_poller()