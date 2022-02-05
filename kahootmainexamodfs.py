from Kahoot import client

client = client.client()

print(client.driver)
client.startGame('https://play.kahoot.it/v2/?quizId=1f76d2dd-4353-4d9a-ab57-71ea9607d050')
client.fetchInfo()

