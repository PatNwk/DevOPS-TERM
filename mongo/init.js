const blogDb = db.getSiblingDB("blog_db");

blogDb.createCollection("posts", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["titre", "auteur", "vues"],
            properties: {
                titre: { bsonType: "string" },
                auteur: { bsonType: "string" },
                vues: { bsonType: "int" }
            }
        }
    },
    validationLevel: "strict",
    validationAction: "error"
});

blogDb.posts.insertMany([
    { titre: "Article_1", auteur: "Gabin", vues: NumberInt(120) },
    { titre: "Article_2", auteur: "Thibaud", vues: NumberInt(95) },
    { titre: "Article_3", auteur: "Arthur", vues: NumberInt(210) },
    { titre: "Article_4", auteur: "Killian", vues: NumberInt(45) },
    { titre: "Article_5", auteur: "Sacha", vues: NumberInt(300) }
]);
