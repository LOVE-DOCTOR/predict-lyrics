import streamlit as st
import joblib
import neattext.functions as nfx


def read_model():
    model = joblib.load('catboost.sav')
    vector = joblib.load('tfidf.sav')

    return model, vector


def preprocess(lyrics):
    lyrics = nfx.fix_contractions(lyrics)

    lyrics = nfx.remove_punctuations(lyrics)

    lyrics = lyrics.lower()

    lyrics = nfx.remove_multiple_spaces(lyrics)

    lyrics = nfx.remove_special_characters(lyrics)
    return lyrics


def main():
    st.set_page_config(page_title='The Music Genre Predictor', layout='wide')
    st.write('<div style="font-weight:bold; font-size:40px;background-clip:text;"><h1>MUSIC GENRE '
             'PREDICTION</h1></div>  ', unsafe_allow_html=True)
    st.subheader('Predict if a song lyric is Rock, Pop, Metal or Jazz')


def predict():
    with st.form(key='music'):
        lyrics = st.text_area("Paste the whole lyrics of the song here")
        submit_button = st.form_submit_button(label='Submit')

    lyrics = preprocess(lyrics)

    if submit_button:
        st.success('Select the "predict" button below')

    if st.button('Predict'):

        model, vector = read_model()

        vectorized = vector.transform([lyrics])
        result = model.predict(vectorized)

        decode = {'Rock': 0, 'Pop': 1, 'Metal': 2, 'Jazz': 3}

        for key, val in decode.items():
            if val == result[0]:
                st.success(f"{key} detected.")


if __name__ == "__main__":
    read_model()
    main()
    predict()
