//
//  GrootUsersService.swift
//  twilight
//
//  Created by Rauhul Varma on 11/11/17.
//  Copyright © 2017 acm. All rights reserved.
//

import Foundation
import APIManager

class GrootUsersService: GrootService {

    override open class var baseURL: String {
        return super.baseURL + "/users"
    }

    class func loginUser(byNetID netID: String, andPassword password: String) -> APIRequest<GrootUsersService, GrootUserContained> {
        return APIRequest<GrootUsersService, GrootUserContained>(endpoint: "/login", body: ["netid": netID, "password": password], method: .POST)
    }

}

