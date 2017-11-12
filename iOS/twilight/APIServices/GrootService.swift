//
//  GrootService.swift
//  twilight
//
//  Created by Rauhul Varma on 11/11/17.
//  Copyright © 2017 acm. All rights reserved.
//

import Foundation
import APIManager

class GrootService: APIService {
    open class var baseURL: String {
        return "https://api.acm.illinois.edu"
    }

    open class var headers: HTTPHeaders? {
        return [
            "Content-Type": "application/json",
            "Authorization": APISecrets.GROOT_CLIENT_KEY
        ]
    }
}
