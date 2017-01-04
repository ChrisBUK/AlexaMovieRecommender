<?php
require_once $_SERVER['DOCUMENT_ROOT'] . '/classes/ApiException.php';
require_once $_SERVER['DOCUMENT_ROOT'] . '/classes/Parameters.php';
require_once $_SERVER['DOCUMENT_ROOT'] . '/classes/AbstractData.php';
require_once $_SERVER['DOCUMENT_ROOT'] . '/classes/DataMovies.php';

// All basic API requests must have a valid method and action parameter.
$strMethod = Parameters::getParam('method', $_GET);
$strAction = Parameters::getParam('action', $_GET);
$strResource = sprintf('%s/%s', $strMethod, $strAction);

try {
    switch ($strResource)
    {

        //get a random movie
        case 'get/randomMovie':
            $objRequest = new DataMovies();
            $strJson = $objRequest->getRandomMovie($_GET);
            break;

        //get a movie by uuid
        case 'get/movieByUuid':
            $objRequest = new DataMovies();
            $strJson = $objRequest->getMovieByUuid($_GET);
            break;

        //get a movie by title
        case 'get/movieByTitle':
            $objRequest = new DataMovies();
            $strJson = $objRequest->getMovieByTitle($_GET);
            break;

        //get a movie by actor
        case 'get/movieByActor':
            $objRequest = new DataMovies();
            $strJson = $objRequest->getRandomMovieByActor($_GET);
            break;            

        //get a movie by genre
        case 'get/movieByGenre':
            $objRequest = new DataMovies();
            $strJson = $objRequest->getRandomMovieByGenre($_GET);
            break;

        //get a movie by actor and genre
        case 'get/movieByActorAndGenre':
            $objRequest = new DataMovies();
            $strJson = $objRequest->getRandomMovieByActorAndGenre($_GET);
            break;

        //get a list of latest movies
        case 'get/latestMovies':
            $objRequest = new DataMovies();
            $strJson = $objRequest->getLatestMovies($_GET);
            break;
     
        //get a list of latest movies by genre
        case 'get/latestMoviesByGenre':
            $objRequest = new DataMovies();
            $strJson = $objRequest->getLatestMoviesByGenre($_GET);
            break;
     
        //get a list of latest movies by actor
        case 'get/latestMoviesByActor':
            $objRequest = new DataMovies();
            $strJson = $objRequest->getLatestMoviesByActor($_GET);
            break;
     
        //get a list of latest movies by actor and genre
        case 'get/latestMoviesByActorAndGenre':
            $objRequest = new DataMovies();
            $strJson = $objRequest->getLatestMoviesByActorAndGenre($_GET);
            break;
     
        //get best rated movies
        case 'get/bestMovies':
            $objRequest = new DataMovies();
            $strJson = $objRequest->getHighestRatedMovies($_GET);
            break;
     
        //get best rated movies by genre
        case 'get/bestMoviesByGenre':
            $objRequest = new DataMovies();
            $strJson = $objRequest->getHighestRatedMoviesByGenre($_GET);
            break;
     
        //get best rated movies by actor
        case 'get/bestMoviesByActor':
            $objRequest = new DataMovies();
            $strJson = $objRequest->getHighestRatedMoviesByActor($_GET);
            break;
     
        //get best rated movies by year
        case 'get/bestMoviesByYear':
            $objRequest = new DataMovies();
            $strJson = $objRequest->getHighestRatedMoviesByYear($_GET);
            break;

        default:
            throw new ApiException("Unrecognised API request: $strResource");
            die;
    }
} catch (ApiException $objException) {
    $objException->gracefulError($objException->getCode());
    die;
}

header("Content-type: text/json");
die($strJson);
?>