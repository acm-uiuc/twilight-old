//
//  GrootReturnDataContainer.swift
//  twilight
//
//  Created by Rauhul Varma on 11/11/17.
//  Copyright © 2017 acm. All rights reserved.
//

import Foundation
import APIManager

class GrootReturnDataContainer<ReturnData: Codable>: Codable, APIReturnable {

    var data: ReturnData?
    var error: String?

    required init(from: Data) throws {
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601

        let decoded = try decoder.decode(GrootReturnDataContainer<ReturnData>.self, from: from)
        data = decoded.data
        error = decoded.error

        assert( (data == nil) != (error == nil) )
    }

}

