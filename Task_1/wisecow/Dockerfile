FROM debian:latest

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y bash fortune-mod cowsay netcat-openbsd && apt-get clean

# Creating symlinks for the binaries
RUN ln -s /usr/games/cowsay /usr/bin/cowsay && ln -s /usr/games/fortune /usr/bin/fortune

EXPOSE 4499

ENV NAME Wisecow

CMD ["./wisecow.sh"]