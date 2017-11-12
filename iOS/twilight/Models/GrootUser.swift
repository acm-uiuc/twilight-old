//
//  GrootUser.swift
//  twilight
//
//  Created by Rauhul Varma on 11/11/17.
//  Copyright © 2017 acm. All rights reserved.
//

import Foundation

typealias GrootUserContained = GrootReturnDataContainer<GrootUser>

class GrootUser: Codable {

    private enum CodingKeys: String, CodingKey {
        case addedToDirectory = "added_to_directory"
        case isMember         = "is_member"
        case createdAt        = "created_at"
        case netID            = "netid"
        case firstName        = "first_name"
        case lastName         = "last_name"
        case token
    }

    var addedToDirectory: Bool
    var isMember: Bool
    var createdAt: Date
    var netID: String
    var firstName: String
    var lastName: String
    var token: String
}
