//
//  SystemStatusViewController.swift
//  twilight
//
//  Created by Rauhul Varma on 11/12/17.
//  Copyright © 2017 acm. All rights reserved.
//

import Foundation
import UIKit

class SystemStatusViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {


    // MARK: - UIViewController


    // MARK: - UITableViewDelegate


    // MARK: - UITableViewDataSource
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 10
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "NodeDetailCell", for: indexPath)
        if let _ = cell as? NodeDetailCell {

        }
        return cell
    }

}
