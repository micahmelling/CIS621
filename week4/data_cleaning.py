import pandas as pd


def main():
    # generate some messy data in a dataframe
    df = pd.DataFrame({
        "books": [
            "A Tale of Two Cities",
            "to kill a mockingbird",
            "\"The Great Gatsby\"",
            "   The Grapes of Wrath",
            "Of mice and men",
            "OLIVER TWIST",
            "Dracula   ",
            "lord of The Rings",
            "Pride and Prejudice,",
            "THE OLD MAN AND THE SEA; Ernest Hemingway",
            "CATCH-22; Joseph Heller"
        ]
    })

    # cast all to lowercase
    df['books'] = df['books'].str.lower()

    # remove leading and trailing spaces
    df['books'] = df['books'].str.strip()

    # remove quotation makes
    df['books'] = df['books'].str.replace('"', '')

    # remove commas
    df['books'] = df['books'].str.replace(',', '')

    # remove authors based on the semi-colon
    df['books'] = df['books'].str.split(';').str[0]

    print(df)


if __name__ == "__main__":
    main()
