<?php
    /**
    * Simple class to sanitize what's being passed in and make sure that we like it.
    * 
    * @author Chris Booker
    */
    class Parameters {

        /**
        * Check a parameter against an allowed list and return a valid value, or a default value, or bool false.
        * 
        * @param mixed $strParamName
        * @param mixed $arrAllowedList
        * @param mixed $strDefault
        */
        
        protected static function getAllowedParam(array $arrParamSource, $strParamName, array $arrAllowedList, $strDefault=null)
        {        
            if (empty($arrParamSource[$strParamName]) || !in_array($arrParamSource[$strParamName], $arrAllowedList))
            {            
                return ($strDefault === null) ? false : $strDefault;
            }
            return $arrParamSource[$strParamName];        
        }

        /**
        * Build a list of parameters based on what is allowed, and what is given, so we can ensure 
        * that other crap doesn't get through.
        * 
        * @param array $arrRequired - parameters that are required
        * @param array $arrOptional - valid parameters that are optional
        * @param array $arrParamSource - a list that is being checked to get required/optional params from.
        */
        public static function getFullParamList(array $arrRequired, array $arrOptional = null, array $arrParamSource = null)
        {
            if ($arrParamSource == null)
            {
                $arrParamSource = $_GET; //Take params from the URL if not otherwise specified.
            }
            $arrParamList = array();

            foreach ($arrRequired as $strParam) 
            {
                $arrParamList[$strParam] = self::getParam($strParam, $arrParamSource);
            }
            
            if ($arrOptional != null)
            {
                foreach ($arrOptional as $strParam)
                {
                    $arrParamList[$strParam] = self::getParam($strParam, $arrParamSource);
                }
            }

            return $arrParamList;
        }

        /**
        * Get a recognised parameter, sanitize it, and return it.
        * 
        * @param string 
        */
        public static function getParam($strParamName, $arrParamSource) 
        {        
            switch ($strParamName) 
            {
                case 'method':
                    $arrAllowList = array('get');
                    $strParamValue = self::getAllowedParam($arrParamSource, 'method', $arrAllowList, 'get');
                    break;

                case 'action':
                    $strParamValue = !empty($arrParamSource['action']) ? $arrParamSource['action'] : null;
                    break;

                case 'uuid':
                    $strParamValue = !empty($arrParamSource['uuid']) ? $arrParamSource['uuid'] : null;
                    break;

                case 'title':
                    $strParamValue = !empty($arrParamSource['title']) ? $arrParamSource['title'] : null;
                    break;
        
                case 'genre':
                    $strParamValue = !empty($arrParamSource['genre']) ? $arrParamSource['genre'] : null;
                    break;

                case 'actor':
                    $strParamValue = !empty($arrParamSource['actor']) ? $arrParamSource['actor'] : null;
                    break;

                case 'year':
                    $strParamValue = !empty($arrParamSource['year']) ? intval($arrParamSource['year']) : null;                

                case 'rating':
                    $strParamValue = !empty($arrParamSource['rating']) ? intval($arrParamSource['rating']) : null;                

                default:
                    return null;
                    break;
            }

            return $strParamValue;
        }
    }
?>