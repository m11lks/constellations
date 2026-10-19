from nicegui import app, ui 
from fastapi import Request
import httpx
from urllib.parse import quote
from vocab import CONSTELLATIONS, LEXICON, PLANETS


def helper_lexicon(key:str) -> str:
      lang = app.storage.user.get('lang','en')
      return LEXICON.get(lang, LEXICON['en']).get(key, key)

def helper_constel(constellation_name:str) -> str:
      lang = app.storage.user.get('lang','en')
      return CONSTELLATIONS.get(lang, CONSTELLATIONS['en']).get(constellation_name, constellation_name)

def helper_planet(planet_name: str) -> str:
    lang = app.storage.user.get('lang', 'en')
    return PLANETS.get(lang, PLANETS['en']).get(planet_name, planet_name)

def switcher_lang():
    def change_lang(w):
        app.storage.user['lang'] = w.value
        ui.navigate.reload()
    current_lang = app.storage.user.get('lang','en')
    ui.select (
         options={'en': 'EN', 'ru': 'RU'},
         value=current_lang,
         label=helper_lexicon('switch language'),
         on_change=change_lang
    ).classes('absolute top-4 right-8 w-20').props('dark')

            
async def cookies_visit(request: Request) -> int: 
    own_count = request.cookies.get('visit_count', '0')
    try:
        count = int(own_count) + 1
    except ValueError:
        count = 1
    await ui.run_javascript(
        f'document.cookie = "visit_count={count}; max-age=31536000; path=/";'
    )
    return count


@ui.page('/')
async def main_page(request:Request):
    ui.query('body').classes('bg-slate-950 text-slate-200')
    await cookies_visit(request)
    switcher_lang()

    async with httpx.AsyncClient(verify=False) as client:
        try:
            res = await client.get('https://127.0.0.1:8000/api/constellation/current')
            data = res.json()

            back_constel_name = data.get('constellation_name', 'Not found')
            back_body_name = data.get('body', 'Cosmos')

            constel_name = helper_constel(back_constel_name)
            body_name = helper_planet(back_body_name)
        except Exception:
            constel_name = helper_lexicon('Not found')
            body_name = helper_lexicon('Not found')


    with ui.row().classes('w-full h-screen items-center justify-between p-8'):
        with ui.card().classes('flex-1 bg-slate-900 p-5 rounded-xl hover:shadow-lg hover:shadow-indigo-500/40 transition'):
                    ui.label(helper_lexicon('search_title')).classes('text-lg font-bold w-full text-center')
                    ui.label(helper_lexicon('search_desc')).classes('w-full text-center')
                    with ui.link(target='/search_page').classes('self-center'):
                        ui.button(helper_lexicon('entry_bt'))

        with ui.card().classes('flex-1 bg-slate-900 p-5 rounded-xl hover:shadow-lg hover:shadow-indigo-500/40 transition'):
               ui.label(body_name).classes('text-sm text-slate-400 w-full text-center')
               ui.label(constel_name).classes('text-lg font-bold w-full text-center')
                    
        with ui.card().classes('flex-1 bg-slate-900 p-5 rounded-xl hover:shadow-lg hover:shadow-indigo-500/40 transition'):
                            ui.label(helper_lexicon('info_title')).classes('text-lg font-bold w-full text-center')
                            ui.label(helper_lexicon('info_desc')).classes('w-full text-center')
                            with ui.link(target='/info_page').classes('self-center'):
                                    ui.button(helper_lexicon('entry_bt'))


@ui.page('/search_page')
def search_page():
    ui.query('body').classes('bg-slate-950 text-slate-200')
    switcher_lang()

    with ui.column().classes('w-full max-w-lg mx-auto items-center justify-center h-screen p-8 gap-4'):
        time_input = ui.input(
            label=helper_lexicon('date_label'), 
            placeholder='YYYY/MM/DD HH:MM:SS', 
            value='2026/09/16 12:00:00'
        ).props('dark').classes('w-full bg-slate-900 rounded-lg px-4')

        lat_input = ui.number(
            label=helper_lexicon('lat_label'), 
            value=55.75, 
            precision=2
        ).props('dark').classes('w-full bg-slate-900 rounded-lg px-4')

        lon_input = ui.number(
            label=helper_lexicon('lon_label'), 
            value=37.61, 
            precision=2
        ).props('dark').classes('w-full bg-slate-900 rounded-lg px-4')


        with ui.card().classes('w-full bg-slate-900 p-5 rounded-xl border border-slate-800 mt-4 items-center'):
            ui.label(helper_lexicon('result_title')).classes('text-xs text-slate-400 uppercase tracking-wider')
            result_label = ui.label(helper_lexicon('ready')).classes('text-lg font-bold text-center text-white')

        async def send_calculation():
            payload = {
                "time_data": str(time_input.value),
                "lat": float(lat_input.value),
                "lon": float(lon_input.value)
            }

            async with httpx.AsyncClient(verify=False) as client:
                try:
                    res = await client.post('https://127.0.0.1:8000/api/calculation', json=payload)
                    
                    res.raise_for_status()
                    data = res.json()

                    translated_name = helper_constel(data['constellation_name'])
                    result_label.text = f"{translated_name} ({data['constellation_code']})"
                    
                except Exception as e:
                    result_label.text = helper_lexicon('conn_err')

        ui.button(helper_lexicon('calc_btn'), on_click=send_calculation).classes('w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-2 rounded-xl transition cursor-pointer') 



@ui.page('/info_page')
async def info_page():

    ui.query('body').classes('bg-slate-950 text-slate-200')
    switcher_lang()

    current_lang = app.storage.user.get('lang', 'en')

    with ui.column().classes(
        'w-full max-w-4xl mx-auto items-center p-8 gap-6 min-h-screen'
    ):

        ui.label(helper_lexicon('info_title')).classes(
            'text-3xl font-bold text-indigo-400'
        )

        with ui.row().classes('w-full gap-2 items-center'):
            search_input = (
                ui.input(
                    value='Astronomy'
                    if current_lang == 'en'
                    else 'Астрономия',
                )
                .props('dark')
                .classes('flex-1 bg-slate-900 rounded-lg px-4')
            )

            search_btn = ui.button(
                'Search' if current_lang == 'en' else 'Искать'
            ).classes(
                'bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-2 px-6 rounded-xl'
            )

        wiki_card = ui.card().classes(
            'w-full bg-slate-900 p-6 rounded-2xl border border-slate-800 gap-4'
        )
        wiki_card.set_visibility(False)

        with wiki_card:
            title_label = ui.label().classes('text-2xl font-bold text-white')

            img_element = ui.image().classes(
                'w-full max-h-80 object-contain rounded-xl bg-slate-950/50'
            )
            img_element.set_visibility(False)

            extract_label = ui.label().classes(
                'text-slate-300 leading-relaxed text-justify'
            )

            wiki_link = ui.link('', target='_blank').classes(
                'text-indigo-400 hover:text-indigo-300 font-semibold self-end mt-2'
            )

        async def load_wiki(query: str = None):
            search_term = (query or search_input.value).strip()
            if not search_term:
                return

            lang = app.storage.user.get('lang', 'en')

            encoded_term = quote(search_term.replace(' ', '_'))
            url = f'https://{lang}.wikipedia.org/api/rest_v1/page/summary/{encoded_term}'

            async with httpx.AsyncClient(follow_redirects=True) as client:
                try:
                    res = await client.get(
                        url, headers={'User-Agent': 'SpaceApp/1.0'}
                    )

                    if res.status_code == 200:
                        data = res.json()

                        title_label.text = data.get('title', '')
                        extract_label.text = data.get(
                            'extract', 'Описание отсутствует.'
                        )

                        if (
                            'thumbnail' in data
                            and 'source' in data['thumbnail']
                        ):
                            img_element.source = data['thumbnail']['source']
                            img_element.set_visibility(True)
                        else:
                            img_element.set_visibility(False)

                        wiki_url = (
                            data.get('content_urls', {})
                            .get('desktop', {})
                            .get('page', '#')
                        )
                        wiki_link.text = (
                            'Read full article'
                            if lang == 'en'
                            else 'Читать полностью на Википедии'
                        )
                        wiki_link.props(f'href="{wiki_url}"')

                        wiki_card.set_visibility(True)
                    else:
                        title_label.text = (
                            'Ничего не найдено'
                            if lang == 'ru'
                            else 'Not found'
                        )
                        extract_label.text = (
                            'Попробуйте изменить поисковый запрос.'
                            if lang == 'ru'
                            else 'Try another search term.'
                        )
                        img_element.set_visibility(False)
                        wiki_link.props('href="#"')
                        wiki_card.set_visibility(True)

                except Exception as e:
                    ui.notify(f'Ошибка загрузки: {e}', type='negative')

        search_btn.on_click(lambda: load_wiki())
        search_input.on('keydown.enter', lambda: load_wiki())
        await load_wiki()

ui.run(port=8080, ssl_keyfile="key.pem", ssl_certfile="cert.pem", storage_secret='private_key')