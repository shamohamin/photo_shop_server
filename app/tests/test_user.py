import json


def test_craete_user_no_email(app, client):
    res = client.post('/user', json={'first_name': 'amin', 'last_name': 'shafie',"password":"123456"})
    assert res.status_code == 400
    expected = {'message': 'please provide email field'}
    assert expected == json.loads(res.get_data(as_text=True))



def test_craete_user(app, client):
    res = client.post('/user', json={'email':'a.sharifzadeh12@gmail.com','first_name': 'ali', 'last_name': 'sharifzadeh',"password":"123456"})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))    
    assert result['token'] is not None


    

def test_craete_user_duplicate_email(app, client):
    res = client.post('/user', json={'email':'a.sharifzadeh12@gmail.com','first_name': 'ali', 'last_name': 'sharifzadeh',"password":"123456"})
    res = client.post('/user', json={'email':'a.sharifzadeh12@gmail.com','first_name': 'ali', 'last_name': 'sharifzadeh',"password":"123456"})
    assert res.status_code == 400
    expected = {'message': 'email already registered!.'}
    assert expected == json.loads(res.get_data(as_text=True))


    

def test_login(app, client):
    res = client.post('/user', json={'email':'a.sharifzadeh12@gmail.com','first_name': 'ali', 'last_name': 'sharifzadeh',"password":"123456"})
    res = client.post('/login', json={'email':'a.sharifzadeh12@gmail.com', "password":"123456"})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))    
    assert result['token'] is not None

        

def test_login_wrong_password(app, client):
    res = client.post('/user', json={'email':'a.sharifzadeh12@gmail.com','first_name': 'ali', 'last_name': 'sharifzadeh',"password":"123456"})
    res = client.post('/login', json={'email':'a.sharifzadeh12@gmail.com', "password":"1234567"})
    assert res.status_code == 403
    expected = {'message': 'email or password was not correct!.'}
    assert expected == json.loads(res.get_data(as_text=True))



        

def test_get_user(app, client):
    res = client.post('/user', json={'email':'a.sharifzadeh12@gmail.com','first_name': 'ali', 'last_name': 'sharifzadeh',"password":"123456"})
    res = client.post('/login', json={'email':'a.sharifzadeh12@gmail.com', "password":"123456"})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))    
    token = result['token']
    res = client.get('/user', headers={'token':token})
    assert res.status_code == 200


    

def test_get_user_wrong_token(app, client):
    res = client.post('/user', json={'email':'a.sharifzadeh12@gmail.com','first_name': 'ali', 'last_name': 'sharifzadeh',"password":"123456"})
    res = client.post('/login', json={'email':'a.sharifzadeh12@gmail.com', "password":"123456"})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))    
    token = result['token']
    res = client.get('/user', headers={'token':'token'})
    assert res.status_code == 401



def test_get_user_by_id(app, client):
    res = client.post('/user', json={'email':'a.sharifzadeh12@gmail.com','first_name': 'ali', 'last_name': 'sharifzadeh',"password":"123456"})
    res = client.post('/login', json={'email':'a.sharifzadeh12@gmail.com', "password":"123456"})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))    
    token = result['token']
    res = client.get('/user', headers={'token':token})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))
    res = client.get('/user/' + str(result['user']['id']), headers={'token':token})
    assert res.status_code == 200

def test_get_user_by_wrong_id(app, client):
    res = client.post('/user', json={'email':'a.sharifzadeh12@gmail.com','first_name': 'ali', 'last_name': 'sharifzadeh',"password":"123456"})
    res = client.post('/login', json={'email':'a.sharifzadeh12@gmail.com', "password":"123456"})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))    
    token = result['token']
    res = client.get('/user', headers={'token':token})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))
    res = client.get('/user/' + str(10), headers={'token':token})
    assert res.status_code == 500

def test_update_first_name_user(app, client):
    res = client.post('/user', json={'email':'a.sharifzadeh13@gmail.com','first_name': 'ali', 'last_name': 'sharifzadeh',"password":"123456"})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))    
    token = result['token']
    res = client.get('/user', headers={'token':token})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))
    res = client.put('/user/' + str(result['user']['id']),json={'email':'a.sharifzadeh13@gmail.com','first_name': 'reza', 'last_name': 'sharifzadeh',"password":"123456"}, headers={'token':token})
    assert res.status_code == 200
    res = client.get('/user', headers={'token':token})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))
    assert result['user']['first_name'] =='reza'

def test_update_last_name_user(app, client):
    res = client.post('/user', json={'email':'a.sharifzadeh14@gmail.com','first_name': 'ali', 'last_name': 'sharifzadeh',"password":"123456"})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))    
    token = result['token']
    res = client.get('/user', headers={'token':token})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))
    res = client.put('/user/' + str(result['user']['id']),json={'email':'a.sharifzadeh14@gmail.com','first_name': 'reza', 'last_name': 'qasemi',"password":"123456"}, headers={'token':token})
    assert res.status_code == 200
    res = client.get('/user', headers={'token':token})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))
    assert result['user']['last_name'] =='qasemi'    


    
def test_delete_user_by_id(app, client):
    res = client.post('/user', json={'email':'a.sharifzadeh15@gmail.com','first_name': 'ali', 'last_name': 'sharifzadeh',"password":"123456"})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))    
    token = result['token']
    res = client.get('/user', headers={'token':token})
    assert res.status_code == 200
    result = json.loads(res.get_data(as_text=True))
    res = client.delete('/user/' + str(result['user']['id']), headers={'token':token})
    assert res.status_code == 202
    res = client.post('/login', json={'email':'a.sharifzadeh12@gmail.com', "password":"123456"})
    assert res.status_code == 400


        

    

    



