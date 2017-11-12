//
//  LoginController.swift
//  twilight
//
//  Created by Rauhul Varma on 11/11/17.
//  Copyright © 2017 acm. All rights reserved.
//

import Foundation
import UIKit

class LoginController {

    static let shared = LoginController()

    private init() { }

    var currentUser: GrootUser?

    func attemptToLoadUserFromDisk() {

    }

    func presentLoginViewController(ifNeeded conditional: Bool, fromViewController controller: UIViewController) {
//        if !conditional {
            let loginViewController = UIStoryboard(name: "Main", bundle: nil).instantiateViewController(withIdentifier: "LoginViewController")
            controller.present(loginViewController, animated: true, completion: nil)
            return
//        }



    }

    func login(user: GrootUser, fromViewController controller: UIViewController) {
        currentUser = user
    }

}
