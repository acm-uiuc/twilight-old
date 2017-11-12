//
//  LoginViewController.swift
//  twilight
//
//  Created by Rauhul Varma on 11/11/17.
//  Copyright © 2017 acm. All rights reserved.
//

import UIKit

class LoginViewController: UIViewController {

    @IBOutlet weak var netIDField: UITextField!
    @IBOutlet weak var passwordField: UITextField!

    @IBAction func login(sender: Any) {
        guard let netID = netIDField.text, let password = passwordField.text else {
                presentErrorViewController(withTitle: "Incomplete", dismissParentOnCompletion: false)
                return
            }

        GrootUsersService.loginUser(byNetID: netID, andPassword: password)
        .onSuccess { (userContainer) in
            if let user = userContainer.data {
                LoginController.shared.login(user: user, fromViewController: self)
            } else {
                let reason = userContainer.error ?? "Unknown error occured. Try again later."
                self.presentErrorViewController(withTitle: "Error", andMessage: reason, dismissParentOnCompletion: false)
            }
        }
        .onFailure { (reason) in
            self.presentErrorViewController(withTitle: "Error", andMessage: reason, dismissParentOnCompletion: false)
        }
        .perform(withAuthorization: nil)
    }


}

