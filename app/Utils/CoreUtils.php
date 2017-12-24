<?php

namespace App\Utils;

/**
 * Description of CoreUtils
 *
 * @author tberdy
 */

class CoreUtils {

    const API_CREDENTIALS = '../resources/credentials/surirobot.json';
    const PROJECT_ID = 'surirobot';

    public static function curlRequest($url, $mode, $contentType, $data = array()) {
        $ch = curl_init();

        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $mode);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array(
            "Content-Type: " . $contentType,
            "Ocp-Apim-Subscription-Key: " . self::API_KEY
        ));
        curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

        $result = curl_exec($ch);
        if (curl_errno($ch)) {
            return response()->json(array(
                        'code' => 400,
                        'msg' => 'Error while contacting the server.'
            ));
        }
        curl_close($ch);

        return json_decode($result);
    }

    public static function saveFile($file) {
        $extension = $file->getClientOriginalExtension();
        $originalFilename = $file->getClientOriginalName();

        $filename = uniqid() . '-' . $originalFilename . '.' . $extension;
        $path = 'storage' . DIRECTORY_SEPARATOR;
        $file->move($path, $filename);

        return ($path . $filename);
    }

}
