import json

import cssutils
from bs4 import BeautifulSoup
from django.conf import settings
from django.db.models import Sum, Avg
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from splinter import Browser
from django.forms.models import model_to_dict

# Create your views here.
from data_scrap.models import Game, Genre, GameUser, Play, Review


def GameItemDetails(request):
    data = {};
    try:
        game = Game.objects.get(pk=request.GET.get('id'));
    except:
        data['result'] = False;
        return HttpResponse(json.dumps(data), content_type='json');

    data['result'] = True;
    data['id'] = game.id;
    data['icon'] = game.icon;
    data['title'] = game.title;
    data['description'] = game.description;
    data['genre'] = [];
    for y in game.genre.all():
        data['genre'].append(y.name);
    return HttpResponse(json.dumps(data), content_type='json');


def AllGame(request):
    games = Game.objects.all();
    allGames = [];
    for x in games:
        data = {};
        data['id'] = x.id;
        data['icon'] = x.icon;
        data['title'] = x.title;
        data['description'] = x.description;
        data['play_count'] = Play.objects.filter(game=x).count();
        data['rating'] = Review.objects.filter(game=x).aggregate(total=Avg('rating'))['total'];

        lastPlayer = Play.objects.filter(game=x).order_by('-time')[0:3]
        data['last_play'] = [];
        for lp in lastPlayer:
            lastPlayerUser = model_to_dict(lp.user);
            print(lastPlayerUser)
            data['last_play'].append({'id': lastPlayerUser['id'], 'userName': lastPlayerUser['userName'],
                                      'userPhoto': lastPlayerUser['userPhoto'].url});
        data['genre'] = [];
        for y in x.genre.all():
            data['genre'].append(y.name);
        allGames.append(data);

    return HttpResponse(json.dumps(allGames), content_type='json');


def ScarpGetGameData(request):
    browser = Browser(driver_name='chrome', executable_path=settings.BASE_DIR + '/chromedriver.exe', headless=True)
    browser.visit("https://rgames.jp/games")
    soup = BeautifulSoup(browser.html, "html.parser")
    list = soup.findAll('div', attrs={'class': 'GameCell'})
    data = [];
    for x in list:
        icon = x.find('div', attrs={'class': 'GameIcon'})['style'];
        gameInfo = {};
        gameInfo['game_id'] = x.find('a')['href'].replace('/games/', '');
        gameInfo['icon'] = cssutils.parseStyle(icon)['background-image'].replace('url(', '').replace(')', '');
        gameInfo['title'] = x.find('span', attrs={'class': 'game-title'}).text;
        gameInfo['description'] = x.findAll('div', attrs={'class': 'description'})[0].text;
        genreData = x.findAll('button', attrs={'class': 'GameGenre'})
        gameInfo['genre'] = [];
        for a in genreData:
            gameInfo['genre'].append(a.text);
        data.append(gameInfo);

    for x in data:
        for y in x['genre']:
            gener = Genre.objects.filter(name=y).first();
            if gener is None:
                gener = Genre(name=y);
                gener.save();
        dataGameId = x['game_id'];
        icon = x['icon'];
        title = x['title'];
        description = x['description'];
        game = Game.objects.filter(id=dataGameId).first();
        if game is None:
            game = Game(id=dataGameId, icon=icon, title=title, description=description);
            game.save();
            for y in x['genre']:
                gener = Genre.objects.filter(name=y).first();
                game.genre.add(gener);
                game.save();
    return HttpResponse(json.dumps(data), content_type='json');


@csrf_exempt
def AddGameUser(request):
    data = {};
    user = GameUser(userName=request.POST['name'], userPhoto=request.FILES['img']);
    user.save();
    data['id'] = user.id;
    data['name'] = user.userName;
    data['photoUrl'] = user.userPhoto.url;
    return HttpResponse(json.dumps(data), content_type='json');
@csrf_exempt
def UserPlayGame(request):
    #print(request.POST['user_id']+" "+request.POST['game_id']);
    gameUser=GameUser.objects.get(pk=request.POST['user_id']);
    gameNow=Game.objects.get(pk=request.POST['game_id']);
    if gameUser:
        print("game user found")
    if gameNow:
        print("game now found..")
    playGame=Play(user=gameUser,game=gameNow);
    playGame.save();
    game=model_to_dict(playGame);
    return HttpResponse(json.dumps(game), content_type='json');

# def GiveRating(request):
#