<?php
    require_once $_SERVER['DOCUMENT_ROOT'] . '/classes/ApiException.php';
    require_once $_SERVER['DOCUMENT_ROOT'] . '/classes/AbstractData.php';

    class DataMovies extends AbstractData
    {
        /** 
        * Get a random movie
        * 
        * @param mixed $arrParams
        */
        public function getRandomMovie(array $arrParams, $strFormat='json')
        {
            $arrRequired = array(); 
            $arrOptional = array();

            if (!self::hasRequiredParameters($arrRequired, $arrParams))
            {
                throw new ApiException("The following parameters are required: ".join(',',$arrRequired), 400);
            }
            
            $arrParams = Parameters::getFullParamList($arrRequired, $arrOptional, $arrParams);

            $strSql = "SELECT *           
                        FROM movie
                        ORDER BY rand()
                        LIMIT 1                      
                        ";
            
            $arrQueryParams = array();
            $objQuery = $this->objDb->prepare($strSql);
            $objQuery->execute($arrQueryParams);
            
            $objResult = new stdClass();
            $objResult->movie = $objQuery->fetch(PDO::FETCH_OBJ);
                        
            return self::formatData($objResult, $strFormat);
        }
        
        public function getMovieByUuid(array $arrParams, $strFormat='json')
        {
            $arrRequired = array('uuid'); 
            $arrOptional = array();

            if (!self::hasRequiredParameters($arrRequired, $arrParams))
            {
                throw new ApiException("The following parameters are required: ".join(',',$arrRequired), 400);
            }
            
            $arrParams = Parameters::getFullParamList($arrRequired, $arrOptional, $arrParams);

            $strSql = "SELECT *           
                        FROM movie
                        WHERE uuid = ?
                        LIMIT 1                      
                        ";
            
            $arrQueryParams = array($arrParams['uuid']);
            $objQuery = $this->objDb->prepare($strSql);
            $objQuery->execute($arrQueryParams);
            
            $objResult = new stdClass();
            $objResult->movie = $objQuery->fetch(PDO::FETCH_OBJ);
                        
            return self::formatData($objResult, $strFormat);
        }

        public function getMovieByTitle(array $arrParams, $strFormat='json')
        {
            $arrRequired = array('title'); 
            $arrOptional = array();

            if (!self::hasRequiredParameters($arrRequired, $arrParams))
            {
                throw new ApiException("The following parameters are required: ".join(',',$arrRequired), 400);
            }
            
            $arrParams = Parameters::getFullParamList($arrRequired, $arrOptional, $arrParams);

            $strSql = "SELECT *           
                        FROM movie
                        WHERE title = ?
                        LIMIT 1                      
                        ";
            
            $arrQueryParams = array($arrParams['title']);
            $objQuery = $this->objDb->prepare($strSql);
            $objQuery->execute($arrQueryParams);
            
            $objResult = new stdClass();
            $objResult->movie = $objQuery->fetch(PDO::FETCH_OBJ);
                        
            return self::formatData($objResult, $strFormat);
        }

        public function getRandomMovieByGenre(array $arrParams, $strFormat='json')
        {
            $arrRequired = array('genre'); 
            $arrOptional = array();

            if (!self::hasRequiredParameters($arrRequired, $arrParams))
            {
                throw new ApiException("The following parameters are required: ".join(',',$arrRequired), 400);
            }
            
            $arrParams = Parameters::getFullParamList($arrRequired, $arrOptional, $arrParams);

            $strSql = "SELECT *           
                        FROM movie
                        WHERE sub_genres like ?
                        ORDER BY rand()
                        LIMIT 1                      
                        ";
            
            $arrQueryParams = array('%'.$arrParams['genre'].'%');
            $objQuery = $this->objDb->prepare($strSql);
            $objQuery->execute($arrQueryParams);
            
            $objResult = new stdClass();
            $objResult->movie = $objQuery->fetch(PDO::FETCH_OBJ);
                        
            return self::formatData($objResult, $strFormat);
        }

        public function getRandomMovieByActor(array $arrParams, $strFormat='json')
        {
            $arrRequired = array('actor'); 
            $arrOptional = array();

            if (!self::hasRequiredParameters($arrRequired, $arrParams))
            {
                throw new ApiException("The following parameters are required: ".join(',',$arrRequired), 400);
            }
            
            $arrParams = Parameters::getFullParamList($arrRequired, $arrOptional, $arrParams);

            $strSql = "SELECT *           
                        FROM movie
                        WHERE cast like ?
                        ORDER BY rand()
                        LIMIT 1                      
                        ";
            
            $arrQueryParams = array('%'.$arrParams['actor'].'%');
            $objQuery = $this->objDb->prepare($strSql);
            $objQuery->execute($arrQueryParams);
            
            $objResult = new stdClass();
            $objResult->movie = $objQuery->fetch(PDO::FETCH_OBJ);
                        
            return self::formatData($objResult, $strFormat);
        }                

    }
?>