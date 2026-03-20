import asyncio
from datetime import UTC, datetime, timedelta
from pathlib import Path

import httpx
from sqlalchemy import delete, select, update

import models
from database import AsyncSessionLocal, engine
from image_utils import PROFILE_PICS_DIR
from main import app

POPULATE_IMAGES_DIR = Path("populate_images")

USERS = [
    {
        "username": "Aegii",
        "email": "CoreyMSchafer@gmail.com",
        "password": "TestPassword1!",
        "image": "Aegir.png",
    },
    {
        "username": "DefaultDude",
        "email": "TestEmail2@test.com",
        "password": "TestPassword2!",
        # No image - uses default
    },
    {
        "username": "Seiba",
        "email": "TestEmail3@test.com",
        "password": "TestPassword3!",
        "image": "SaberAlt.jpg",
    },
    {
        "username": "SwordGuy999",
        "email": "TestEmail4@test.com",
        "password": "TestPassword4!",
        "image": "sword.jpg",
    },
    {
        "username": "HouHouinKyouma",
        "email": "TestEmail5@test.com",
        "password": "TestPassword5!",
        "image": "FG.jpg",
    },
    {
        "username": "Celeb17",
        "email": "TestEmail6@test.com",
        "password": "TestPassword6!",
        "image": "kurisu.png",
    },
]

POSTS = [
    {
        "title": "Shirou and the art of overcooking life",
        "content": "Shirou cannot just cook a meal like a normal person. Every time he touches a pan it feels like he's about to sacrifice his entire existence for a bowl of soup. Bro is standing there like he's forging Excalibur instead of making breakfast. At this point I’m convinced the rice cooker has seen more character development than half the cast."
    },
    {
        "title": "Rin tsundere allegations",
        "content": "Rin will risk her life, spend all her gems, and still say 'it's not like I care.' At this point it's not denial, it's a full-time occupation with benefits. Even the enemies can tell what's going on before Shirou does. She could confess directly and still somehow phrase it like an insult."
    },
    {
        "title": "Archer really said I hate my younger self",
        "content": "Imagine growing up just to become your own biggest hater. Archer saw Shirou and immediately decided this man needs to be stopped at all costs. That's not even character conflict, that's self-targeted harassment. Honestly, it's kind of relatable after a bad life decision."
    },
    {
        "title": "Saber",
        "content": "Saber can fight legendary heroes with centuries of experience, but she would surrender for a burger ToT. Seiba seiba Seiba seiba Seiba seiba Seiba seiba ~~ "
    },
    {
        "title": "Gilgamesh wakes up arrogant every day",
        "content": "Some people build confidence over time, Gilgamesh just spawned with max stats. The man has never doubted himself once and probably never will. Even when he's wrong, he's wrong with confidence. You almost have to respect the consistency at that level."
    },
    {
        "title": "why are we debating mid fight",
        "content": "Fate fights always start intense and then suddenly someone starts a philosophy lecture. You're watching a sword clash and then boom, existential crisis. Like bro, why are we discussing morality while airborne? Can we finish the fight first and debate later?"
    },
    {
        "title": "Kirei is just evil for fun",
        "content": "Kirei doesn't even need a reason anymore, he's just doing side quests in villainy. The man wakes up and chooses chaos like it's part of his daily routine. He smiles like he just unlocked a new achievement in being a menace. Honestly, he's having way too much fun."
    },
    {
        "title": "Lancer deserves better honestly",
        "content": "Every time Lancer shows up you already know it's not going to end well. It's like the universe personally scheduled his downfall. He doesn't even get a chance to relax before something goes wrong. At this point it's less bad luck and more a scripted event."
    },
    {
        "title": "Steins Gate tricked me",
        "content": "I thought I was watching a goofy science anime with random experiments. Everything felt light and chaotic in a fun way. Then suddenly the tone shifts and you're emotionally compromised. I did not sign up for this level of suffering."
    },
    {
        "title": "Okabe vs common sense",
        "content": "Okabe talks like he's running a global conspiracy but forgets basic logic sometimes. He’ll say something dramatic and then immediately contradict himself. The confidence is unreal though, you almost believe him anyway. That lab coat really carries his authority."
    },
    {
        "title": "Tuturu is not harmless",
        "content": "At first it's cute and feels like a harmless catchphrase. Then the context changes and suddenly it hits different. That single word starts carrying emotional weight you weren't ready for. Now every time you hear it, you feel uneasy."
    },
    {
        "title": "Kurisu carrying the entire plot",
        "content": "Without Kurisu, nothing in the lab would function properly. She’s basically the only one applying logic while everyone else is improvising chaos. Every breakthrough somehow traces back to her. She's not just a character, she's the backbone of the entire operation."
    },
    {
        "title": "Daru is way too realistic",
        "content": "Out of everyone in the lab, Daru feels the most grounded somehow. Not because he's normal, but because he reacts like someone who should not be involved in time travel. He's just there vibing and suddenly responsible for major events. It's both hilarious and concerning."
    },
    {
        "title": "time travel was a mistake",
        "content": "Every single time someone changes the timeline, things somehow get worse. You fix one problem and create three new ones. At some point you have to accept the universe does not want your help. Just leave it alone and go home."
    },
    {
        "title": "Shirou logic strikes again",
        "content": "Shirou says things that sound deep until you actually think about them. Then you realize it barely makes sense. But the way he delivers it makes you question yourself instead. Confidence really is half the battle."
    },
    {
        "title": "UBW is just self argument simulator",
        "content": "Unlimited Blade Works is basically Shirou arguing with himself for hours. It’s like watching a debate where both sides refuse to back down. Somehow both are right and wrong at the same time. It's exhausting but also kind of impressive."
    },
    {
        "title": "Heavens Feel is not okay",
        "content": "You go into this route expecting a romance and come out emotionally destroyed. The tone shift is not gentle at all. It just drops you into darkness and expects you to deal with it. Happiness feels like a distant concept here."
    },
    {
        "title": "Gilgamesh does not fight fair",
        "content": "He doesn't duel like a normal person. He just spams weapons like he's playing a game with unlimited resources. Imagine trying your best and your opponent has infinite inventory. It's not a fight, it's a flex."
    },
    {
        "title": "why is fate so complicated",
        "content": "Trying to explain Fate to someone feels impossible. You start with a simple premise and then it spirals into timelines, routes, and alternate versions. By the end you're confused too. It's a shared experience at this point."
    },
    {
        "title": "Okabe laugh hits different",
        "content": "At first it's awkward and kind of cringe. Then it grows on you slowly. Eventually it becomes iconic and you can't imagine him without it. Character development through laughter is real."
    },
    {
        "title": "Okabe and Kurisu are basically married already",
        "content": "They argue constantly but there's clearly something there. It's that dynamic where they pretend to be annoyed but care deeply. The chemistry is obvious from the start. They just refuse to acknowledge it."
    },
    {
        "title": "Mayuri needs to be protected",
        "content": "There is no deeper analysis needed here. She deserves peace and happiness, that's it. No debate, no counterargument. Just protect her."
    },
    {
        "title": "Daru typing is actually insane",
        "content": "The way Daru types makes no sense. It looks like he's hitting random keys and suddenly something works. You blink and he's already done something important. It's chaotic but effective."
    },
    {
        "title": "Servants are more interesting than masters",
        "content": "You expect the masters to be the focus, but the servants steal the show. They have more personality and more dramatic backstories. Every interaction feels bigger with them involved. It's hard not to get attached."
    },
    {
        "title": "Kirei's Mapo Tofu",
        "content": "Why does this man eat like it's part of his character arc? Even something simple feels unsettling when he does it. You can’t trust someone who enjoys food like that."
    },
    {
        "title": "this anime hurt me",
        "content": "I started watching casually with no expectations. Somewhere along the way it became personal. Now I'm emotionally invested and slightly damaged. This was not the plan."
    },
    {
        "title": "Okabe needs professional help",
        "content": "At some point this stops being funny. The amount of stress he's under is unreal. Someone needs to step in and help him process everything. This is not sustainable."
    },
    {
        "title": "Rin has unlimited money apparently",
        "content": "She throws gems around like they're nothing. Meanwhile I'm thinking about my budget. The difference in financial reality is wild. She lives in a different economy."
    },
    {
        "title": "Berserker solves problems differently",
        "content": "Strategy is optional when brute force works every time. Why think when you can just hit harder? It's simple but effective. You can't argue with results."
    },
    {
        "title": "Illya is terrifying actually",
        "content": "She looks harmless at first glance. Then you realize there's something very off. That contrast makes it even worse. It's unsettling in the best way."
    },
    {
        "title": "why is every attack a speech",
        "content": "No one just attacks immediately. Everyone needs to explain their ability first. It's like a presentation before action. Imagine doing that in real life."
    },
    {
        "title": "the microwave incident",
        "content": "Only in this show does a microwave become a major plot device. Something so normal turns into something dangerous. It's both ridiculous and impressive."
    },
    {
        "title": "Christina will never escape that name",
        "content": "She clearly doesn't like it, but it's already too late. The nickname stuck instantly. There's no going back from that."
    },
    {
        "title": "should we trust daru with anything",
        "content": "He's incredibly skilled but also unpredictable. You want to trust him but there's hesitation. It's a risky situation either way. Somehow it still works out."
    },
    {
        "title": "Shirou refuses to be normal",
        "content": "Every time there's a reasonable option, he chooses something else. It's consistent at least. You know what to expect from him. Just not logic."
    },
    {
        "title": "Saber just wants to eat",
        "content": "After everything she's been through, food is her comfort. It’s one of the few simple joys she has. Honestly, it’s relatable."
    },
    {
        "title": "Gilgamesh ego expansion pack",
        "content": "If ego was something you could upgrade, he maxed it out. There's no limit in sight. It just keeps going. It's impressive in a way."
    },
    {
        "title": "that ending was worth it",
        "content": "After everything that happens, the ending feels earned. You go through a lot to get there. It hits harder because of the journey."
    },
    {
        "title": "Fate watch order is a boss fight",
        "content": "You don't just watch Fate casually. You prepare mentally first. Figuring out where to start is half the challenge. It's an experience on its own."
    },
    {
        "title": "rewatching makes it worse",
        "content": "You notice things you didn't catch before. Small details suddenly make sense. And somehow it hurts more the second time."
    },
    {
        "title": "why am I emotionally attached now",
        "content": "I started watching without expectations. Now I'm invested in every character. This was not supposed to happen."
    }
]

# The 42th post - always the oldest
POST_42 = {
    "title": "This is the 42th post....",
    "content": "Paginate to this 42th post and get to learn this fun fact: In Douglas Adams' The Hitchhiker's Guide to the Galaxy, 42 is the answer given by a supercomputer to “the Ultimate Question of Life, the Universe, and Everything.” And also it is the answer to.... 6 x 7 :3",
}


async def clear_existing_data() -> None:
    # Delete profile pictures from local storage
    if PROFILE_PICS_DIR.exists():
        for file in PROFILE_PICS_DIR.iterdir():
            if file.is_file() and file.name != ".gitkeep":
                file.unlink()
        print(f"Deleted profile pictures from {PROFILE_PICS_DIR}")

    # Clear database tables (order respects foreign keys)
    async with AsyncSessionLocal() as db:
        await db.execute(delete(models.Post))
        await db.execute(delete(models.User))
        await db.commit()
    print("Cleared existing data")


async def update_post_dates() -> None:
    now = datetime.now(UTC)

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(models.Post).order_by(models.Post.id))
        posts = result.scalars().all()

        if not posts:
            return

        # First post (POST_42) is the oldest - ~90 days ago
        await db.execute(
            update(models.Post)
            .where(models.Post.id == posts[0].id)
            .values(date_posted=now - timedelta(days=90)),
        )

        # Remaining posts: each ~1.5 days newer than previous
        for i, post in enumerate(posts[1:], start=1):
            days_ago = (len(posts) - i) * 1.5
            hours_offset = (i * 7) % 24
            post_date = now - timedelta(days=days_ago, hours=hours_offset)
            await db.execute(
                update(models.Post)
                .where(models.Post.id == post.id)
                .values(date_posted=post_date),
            )

        await db.commit()
    print("Updated post dates")


async def populate() -> None:
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://localhost",
    ) as client:
        # Clear existing data (local images first, then database)
        await clear_existing_data()

        users: list[dict] = []

        print(f"\nCreating {len(USERS)} users...")
        for user_data in USERS:
            response = await client.post(
                "/api/users",
                json={
                    "username": user_data["username"],
                    "email": user_data["email"],
                    "password": user_data["password"],
                },
            )
            response.raise_for_status()
            user = response.json()
            print(f"  Created: {user['username']}")

            response = await client.post(
                "/api/users/token",
                data={
                    "username": user_data["email"],
                    "password": user_data["password"],
                },
            )
            response.raise_for_status()
            token = response.json()["access_token"]

            if image_name := user_data.get("image"):
                image_path = POPULATE_IMAGES_DIR / image_name
                if image_path.exists():
                    response = await client.patch(
                        f"/api/users/{user['id']}/picture",
                        files={
                            "file": (
                                image_name,
                                image_path.read_bytes(),
                                "image/png",
                            ),
                        },
                        headers={"Authorization": f"Bearer {token}"},
                    )
                    response.raise_for_status()
                    print(f"    Uploaded: {image_name}")

            users.append(
                {"id": user["id"], "username": user["username"], "token": token},
            )

        print(f"\nCreating {len(POSTS) + 1} posts...")

        # First create POST_42 (will become oldest after date update)
        response = await client.post(
            "/api/posts",
            json={"title": POST_42["title"], "content": POST_42["content"]},
            headers={"Authorization": f"Bearer {users[0]['token']}"},
        )
        response.raise_for_status()
        print(f"  Created: '{POST_42['title']}'")

        # Create remaining posts in reverse (last in list = oldest, first = newest)
        for i, post_data in enumerate(reversed(POSTS)):
            user = users[i % len(users)]
            response = await client.post(
                "/api/posts",
                json={
                    "title": post_data["title"],
                    "content": post_data["content"],
                },
                headers={"Authorization": f"Bearer {user['token']}"},
            )
            response.raise_for_status()
            title = post_data["title"]
            print(
                f"  Created: '{title[:50]}...'"
                if len(title) > 50
                else f"  Created: '{title}'",
            )

        print("\nUpdating post dates...")
        await update_post_dates()

    await engine.dispose()

    print("\nDone!")
    print(f"  {len(USERS)} users")
    print(f"  {len(POSTS) + 1} posts")
    print("  Profile pictures saved locally")


if __name__ == "__main__":
    asyncio.run(populate())