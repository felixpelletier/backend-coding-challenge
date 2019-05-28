[![Build Status](https://travis-ci.org/felixpelletier/backend-coding-challenge.svg?branch=master)](https://travis-ci.org/felixpelletier/backend-coding-challenge)

# Coveo Backend Coding Challenge
(inspired by https://github.com/busbud/coding-challenge-backend-c)

## Link to Heroku

[https://felixpelletier-coveo-challenge.herokuapp.com/suggestions](https://felixpelletier-coveo-challenge.herokuapp.com/suggestions?q=)

## Implementation

The "suggestion engine" uses multiple metrics with configurable weights.
Each metric is given the full query and some information about a city.
They assign a score from 0.0 to 1.0 for each city.
Scores are then combined according to the metric's given weight.

### Metrics

#### NameStartsWith:
 This metric assigns a perfect score to a query which is exactly the beginning of a city's name.
 It is ignored from the score calculation if this is not the case.
 This skews the results towards the right city if the user writes it perfectly.
 
 Ex: With query "Queb", the city "Quebec" gets a perfect score.

#### LevenshteinCityNameSimilarity: 
  The score is computed according to number of edits needed to transform the query into the city's name.
  
#### HaversineLocationDistance:
  The score is computed according to the city's distance to the location given in the query, if one was given. 
 
#### LogarithmicPopulation:
  This metric favors more populated cities, as they may be more likely to be searched by the user.  
 

### Configuration

Each metrics can be configured using the *metrics_config.yaml* file.

There is currently only one parameter (the weight).

Here's an example:

```yaml
NameStartsWith:
  weight: 10

LevenshteinCityNameSimilarity:
  weight: 7

HaversineLocationDistance:
  weight: 3

LogarithmicPopulation:
  weight: 3
```

## Skill development

- This wasn't my first Python project, but my I was a little rusty.

This was my first time:
- Trying out the type hints capabilities of Python.
- Trying out Googles import style (full import path, import only modules). 
- Using Flask.
- Using Heroku.
- Using Yaml.
- Configuring Travis CI (more used to Jenkins).
  
## What would have been nice to try

### Design

 - Have the metrics be a little more modular, with the ability to add
   some new ones simply by importing a new package.
 - Adding the ability to configure each metric with their own specific options.
 - Adding some logic between the metrics, such as checking distances only if the name is similar enough.
 
### Performance

If necessary:
 - Have some way of pruning cities quickly. 
   Maybe have some threshold on some metrics. 
   If below a certain threshold, just prune the city.
 - Add a cache for common queries.
  
### Tools
 - Trying out a static type checker, such as mypy or Microsoft's pyright.
 - Trying out a load tester, such as Locust.
 - Adding a style checker and some linter (ex: pylint) as commit tests.
 - Automating the requirements.txt generation on commit.

************************************************************************************************************************

# Original README

# Coveo Backend Coding Challenge
(inspired by https://github.com/busbud/coding-challenge-backend-c)

## Requirements

Design a REST API endpoint that provides auto-complete suggestions for large cities.

- The endpoint is exposed at `/suggestions`
- The partial (or complete) search term is passed as a querystring parameter `q`
- The caller's location can optionally be supplied via querystring parameters `latitude` and `longitude` to help improve relative scores
- The endpoint returns a JSON response with an array of scored suggested matches
    - The suggestions are sorted by descending score
    - Each suggestion has a score between 0 and 1 (inclusive) indicating confidence in the suggestion (1 is most confident)
    - Each suggestion has a name which can be used to disambiguate between similarly named locations
    - Each suggestion has a latitude and longitude

## "The rules"

- *You can use the language and technology of your choosing.* It's OK to try something new (tell us if you do), but feel free to use something you're comfortable with. We don't care if you use something we don't; the goal here is not to validate your knowledge of a particular technology.
- End result should be deployed on a public Cloud (Heroku, AWS etc. all have free tiers you can use).

## Advice

- **Try to design and implement your solution as you would do for real production code**. Show us how you create clean, maintainable code that does awesome stuff. Build something that we'd be happy to contribute to. This is not a programming contest where dirty hacks win the game.
- Documentation and maintainability are a plus, and don't you forget those unit tests.
- We don’t want to know if you can do exactly as asked (or everybody would have the same result). We want to know what **you** bring to the table when working on a project, what is your secret sauce. More features? Best solution? Thinking outside the box?

## Can I use a database?

If you wish, it's OK to use external systems such as a database, an Elastic index, etc. in your solution. But this is certainly not required to complete the basic requirements of the challenge. Keep in mind that **our goal here is to see some code of yours**; if you only implement a thin API on top of a DB we won't have much to look at.

Our advice is that if you choose to use an external search system, you had better be doing something really truly awesome with it.

## Sample responses

These responses are meant to provide guidance. The exact values can vary based on the data source and scoring algorithm

**Near match**

    GET /suggestions?q=Londo&latitude=43.70011&longitude=-79.4163

```json
{
  "suggestions": [
    {
      "name": "London, ON, Canada",
      "latitude": "42.98339",
      "longitude": "-81.23304",
      "score": 0.9
    },
    {
      "name": "London, OH, USA",
      "latitude": "39.88645",
      "longitude": "-83.44825",
      "score": 0.5
    },
    {
      "name": "London, KY, USA",
      "latitude": "37.12898",
      "longitude": "-84.08326",
      "score": 0.5
    },
    {
      "name": "Londontowne, MD, USA",
      "latitude": "38.93345",
      "longitude": "-76.54941",
      "score": 0.3
    }
  ]
}
```

**No match**

    GET /suggestions?q=SomeRandomCityInTheMiddleOfNowhere

```json
{
  "suggestions": []
}
```

## References

- Geonames provides city lists Canada and the USA http://download.geonames.org/export/dump/readme.txt

## Getting Started

Begin by forking this repo and cloning your fork. GitHub has apps for [Mac](http://mac.github.com/) and
[Windows](http://windows.github.com/) that make this easier.
