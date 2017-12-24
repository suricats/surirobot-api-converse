<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Utils\CoreUtils;
use Google\Cloud\Speech\SpeechClient;

function array_empty($array) {
   $is_empty = true;
   foreach($array as $k) {
      $is_empty = $is_empty && empty($k);
   }
   return $is_empty;
}

class RecognizeController extends Controller {

    /**
     * Operation recognizePost
     *
     * Recognize text from audio file.
     *
     *
     * @return Http response
     */
    public function recognizePost(Request $request) {
        $input = $request->all();
        if (!isset($input['audio'])) {
            throw new \InvalidArgumentException('Missing the required parameter $audio when calling identifyPost');
        }
        if (!isset($input['language'])) {
            $language = 'fr-FR';
        }
        else
            $language = $input['language'];
        $audio = $input['audio'];
        $filepath = CoreUtils::saveFile($audio);


        $speech = new SpeechClient([
            'projectId' => CoreUtils::PROJECT_ID,
            'keyFilePath' => CoreUtils::API_CREDENTIALS,
            'languageCode' => $language,
        ]);

        $options = [
            'encoding' => 'LINEAR16',
            //'sampleRateHertz' => 44100,
        ];
        
        $results = $speech->recognize(fopen($filepath, 'r'), $options);

        $data = array();
        $confid = array();
        foreach ($results as $result) {
            $data[] = $result->alternatives()[0]['transcript'];
            $confid[] = $result->alternatives()[0]['confidence'];
        }
        if (array_empty($data)){
            return response()->json(array(
                        'code' => 210,
                        'msg' => 'No voice was heard'
            ));
        }

        return response()->json(array(
                    'code' => 200,
                    'msg' => 'OK',
                    'data' => array(
                        'text' => $data,
                    ),
                    'confidence' => array(
                        'percentage' => $confid,
                    )
        ));
    }

}
